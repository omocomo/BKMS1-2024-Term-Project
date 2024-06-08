import psycopg2
import numpy as np
import pandas as pd
import re
from sqlalchemy.future import select
from .models import Product
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sentence_transformers import SentenceTransformer

# 모델 초기화
model = SentenceTransformer('bespin-global/klue-sroberta-base-continue-learning-by-mnr')

# 최종 스코어 계산 함수
async def calculate_final_scores(db: AsyncSession, user_vector):
    # user_vector를 SQL 쿼리에 맞게 변환
    user_vector_query = f"""
    WITH user_vector AS (
        SELECT
            {user_vector['reviewer_id']} AS reviewer_id,
            {user_vector['skin_type_oily']}::boolean AS skin_type_oily,
            {user_vector['skin_concern_excess_sebum']}::boolean AS skin_concern_excess_sebum,
            {user_vector['skin_type_trouble_prone']}::boolean AS skin_type_trouble_prone,
            {user_vector['skin_type_sensitive']}::boolean AS skin_type_sensitive,
            {user_vector['skin_concern_trouble']}::boolean AS skin_concern_trouble,
            {user_vector['skin_concern_atopy']}::boolean AS skin_concern_atopy,
            {user_vector['skin_type_combination']}::boolean AS skin_type_combination,
            {user_vector['skin_type_normal']}::boolean AS skin_type_normal,
            {user_vector['skin_concern_whitening']}::boolean AS skin_concern_whitening,
            {user_vector['skin_concern_wrinkles']}::boolean AS skin_concern_wrinkles,
            {user_vector['skin_type_dry']}::boolean AS skin_type_dry,
            {user_vector['skin_type_mildly_dry']}::boolean AS skin_type_mildly_dry
    )
    """
    # print(user_vector_query)
    # 전체 SQL 쿼리
    query = f"""
    {user_vector_query},
    global_mean AS (
        SELECT
            AVG((
                COALESCE(skin_type_oily::int, 0) + 
                COALESCE(cleansing_power_very_satisfied::int, 0) + 
                COALESCE(skin_concern_soothing::int, 0) +
                COALESCE(irritation_level_not_irritating::int, 0) + 
                COALESCE(skin_type_combination::int, 0) +
                COALESCE(skin_concern_wrinkles_whitening::int, 0) + 
                COALESCE(skin_type_dry::int, 0)
            )::float) AS mean_score
        FROM product
    ),
    product_scores AS (
        SELECT
            p.product_id,
            p.product_name,
            p.brand_name,
            p.number_of_reviews,
            (COALESCE(u.skin_type_oily::int, 0) * COALESCE(p.skin_type_oily::int, 0) +
             COALESCE(u.skin_concern_excess_sebum::int, 0) * COALESCE(p.cleansing_power_very_satisfied::int, 0) +
             (COALESCE(u.skin_type_trouble_prone::int, 0) + COALESCE(u.skin_type_sensitive::int, 0) + 
              COALESCE(u.skin_concern_trouble::int, 0) + COALESCE(u.skin_concern_atopy::int, 0)) * COALESCE(p.skin_concern_soothing::int, 0) +
             (COALESCE(u.skin_type_trouble_prone::int, 0) + COALESCE(u.skin_type_sensitive::int, 0) + 
              COALESCE(u.skin_concern_trouble::int, 0) + COALESCE(u.skin_concern_atopy::int, 0)) * COALESCE(p.irritation_level_not_irritating::int, 0) +
             (COALESCE(u.skin_type_combination::int, 0) + COALESCE(u.skin_type_normal::int, 0)) * COALESCE(p.skin_type_combination::int, 0) +
             (COALESCE(u.skin_concern_whitening::int, 0) + COALESCE(u.skin_concern_wrinkles::int, 0)) * COALESCE(p.skin_concern_wrinkles_whitening::int, 0) +
             (COALESCE(u.skin_type_dry::int, 0) + COALESCE(u.skin_type_mildly_dry::int, 0)) * COALESCE(p.skin_type_dry::int, 0)
            ) AS raw_score
        FROM product p, user_vector u
        WHERE p.number_of_reviews >= 100
    ),
    z_scores_product AS (
        SELECT
            product_id,
            raw_score,
            (raw_score - AVG(raw_score) OVER ()) / STDDEV(raw_score) OVER () AS z_score
        FROM product_scores
    ),
    similar_users AS (
        SELECT
            r.reviewer_id,
            (r.skin_type_oily::int * u.skin_type_oily::int +
             r.skin_concern_excess_sebum::int * u.skin_concern_excess_sebum::int +
             (r.skin_type_trouble_prone::int + r.skin_type_sensitive::int + 
              r.skin_concern_trouble::int + r.skin_concern_atopy::int) * 
              (u.skin_type_trouble_prone::int + u.skin_type_sensitive::int + 
               u.skin_concern_trouble::int + u.skin_concern_atopy::int) +
             (r.skin_type_combination::int + r.skin_type_normal::int) * 
              (u.skin_type_combination::int + u.skin_type_normal::int) +
             (r.skin_concern_whitening::int + r.skin_concern_wrinkles::int) * 
              (u.skin_concern_whitening::int + u.skin_concern_wrinkles::int) +
             (r.skin_type_dry::int + r.skin_type_mildly_dry::int) * 
              (u.skin_type_dry::int + u.skin_type_mildly_dry::int)
            ) AS similarity
        FROM reviewer r, user_vector u
    ),
    filtered_users AS (
        SELECT reviewer_id
        FROM similar_users
        WHERE similarity >= 2
    ),
    similar_reviews AS (
        SELECT
            product_id,
            (r.rating * (CASE WHEN r.repurchase_intention THEN 1.5 ELSE 1 END)) AS weighted_rating
        FROM review r
        WHERE r.reviewer_id IN (SELECT reviewer_id FROM filtered_users)
    ),
    average_ratings AS (
        SELECT
            product_id,
            SUM(weighted_rating) / COUNT(*) AS avg_rating
        FROM similar_reviews
        GROUP BY product_id
    ),
    z_scores_similar_users AS (
        SELECT
            product_id,
            (avg_rating - AVG(avg_rating) OVER ()) / STDDEV(avg_rating) OVER () AS z_score
        FROM average_ratings
    ),
    brand_scores AS (
        SELECT
            p.brand_name,
            AVG(zp.z_score) AS avg_brand_score
        FROM z_scores_product zp
        JOIN product p ON zp.product_id = p.product_id
        GROUP BY p.brand_name
    ),
    z_scores_brand AS (
        SELECT
            brand_name,
            (avg_brand_score - AVG(avg_brand_score) OVER ()) / STDDEV(avg_brand_score) OVER () AS z_score
        FROM brand_scores
    ),
    final_scores AS (
        SELECT
            p.product_id,
            p.product_name,
            p.brand_name,
            zp.z_score AS product_score,
            zs.z_score AS similar_user_score,
            zb.z_score AS brand_score,
            0.2 * zp.z_score + 0.7 * zs.z_score + 0.1 * zb.z_score AS final_score,
            p.number_of_reviews
        FROM product p
        LEFT JOIN z_scores_product zp ON p.product_id = zp.product_id
        LEFT JOIN z_scores_similar_users zs ON p.product_id = zs.product_id
        LEFT JOIN z_scores_brand zb ON p.brand_name = zb.brand_name
        WHERE 0.2 * zp.z_score + 0.7 * zs.z_score + 0.1 * zb.z_score >= 0
        ORDER BY final_score DESC
    )
    SELECT * FROM final_scores;
    """
    # 쿼리 실행
    result = await execute_custom_query(db, text(query))
    return result

async def get_top_products_by_similarity(db: AsyncSession, query: str, alpha=1.0, beta=1.0, gamma=1.5, top_n=None):
    # 쿼리를 임베딩 벡터로 변환
    query_embedding = model.encode([query])[0].tolist()

    # product_similarities 테이블이 존재하면 삭제
    await db.execute(text("DROP TABLE IF EXISTS product_similarities"))
    
    # 제품명 임베딩과의 유사도 계산
    product_name_similarities_query = """
    CREATE TABLE product_similarities AS
    WITH query_embedding AS (
        SELECT '%s'::vector AS embedding
    ),
    product_similarities AS (
        SELECT
            p.product_id,
            p.product_name,
            1 - (p.product_name_embedding <=> (SELECT embedding FROM query_embedding)) AS name_similarity
        FROM
            product p
    )
    SELECT * FROM product_similarities;
    """ %(query_embedding)
    await db.execute(text(product_name_similarities_query))
    await db.commit()

    result = await db.execute(text("SELECT * FROM product_similarities"))
    product_name_similarities = result.fetchall()

    # 리뷰 임베딩과의 유사도 계산 및 제품별 평균 유사도 계산
    review_similarities_query = """
    WITH query_embedding AS (
        SELECT '%s'::vector AS embedding
    ),
    review_similarities AS (
        SELECT
            r.product_id,
            1 - (r.review_content_embedding <=> (SELECT embedding FROM query_embedding)) AS review_similarity,
            r.used_over_one_month
        FROM
            review r
    ),
    product_review_aggregates AS (
        SELECT
            rs.product_id,
            COUNT(*) AS review_count,
            SUM(CASE WHEN rs.used_over_one_month = True THEN 1 ELSE 0 END) AS used_count,
            AVG(rs.review_similarity) AS avg_similarity,
            AVG(CASE WHEN rs.used_over_one_month = True THEN rs.review_similarity ELSE NULL END) AS avg_similarity_used
        FROM
            review_similarities rs
        GROUP BY
            rs.product_id
    ),
    final_scores AS (
        SELECT
            pr.product_id,
            ps.name_similarity,
            pr.review_count,
            pr.used_count,
            pr.avg_similarity,
            COALESCE(pr.avg_similarity_used, 0) AS avg_similarity_used,
            CASE
                WHEN pr.review_count >= 3 THEN
                    (ps.name_similarity * %s + pr.avg_similarity * %s + COALESCE(pr.avg_similarity_used * %s, 0)) / (1 + %s + COALESCE(pr.used_count * %s, 0))
                ELSE
                    (ps.name_similarity * %s + pr.avg_similarity * %s) / (1 + %s)
            END AS final_score
        FROM
            product_review_aggregates pr
            JOIN product_similarities ps ON pr.product_id = ps.product_id
    )
    SELECT * FROM final_scores ORDER BY final_score DESC LIMIT %s;
    """ %(query_embedding, alpha, beta, gamma, gamma, gamma, alpha, beta, alpha + beta, top_n)
    result = await db.execute(text(review_similarities_query))
    final_scores = result.fetchall()

    # 결과 정리 및 출력
    result_df = pd.DataFrame(final_scores, columns=['product_id', 'name_similarity', 'review_count', 'used_count', 'avg_similarity', 'avg_similarity_used', 'final_score'])
    
    return result_df

async def create_view_from_df(db: AsyncSession, df, view_name, query):
    # 정확히 일치하는 단어가 있는지 확인
    for keyword in FILTER_KEYWORDS:
        if check_exact_match(query, keyword):
            filtered_df = df[df['product_id'].isin(await get_filtered_product_ids(db, keyword))]
            df = filtered_df
            break

    df_tuples = df.itertuples(index=False, name=None)
    values = ', '.join([f"({', '.join(map(str, row))})" for row in df_tuples])# ', '.join(db.mogrify('(%s,%s,%s,%s,%s,%s,%s)', row).decode('utf-8') for row in df_tuples)
    create_view_query = f"""
    CREATE OR REPLACE VIEW {view_name} AS
    SELECT 
        p.*, 
        t.name_similarity,
        t.review_count,
        t.used_count,
        t.avg_similarity,
        t.avg_similarity_used,
        t.final_score
    FROM 
        product p
    JOIN 
        (VALUES {values}) AS t(product_id, name_similarity, review_count, used_count, avg_similarity, avg_similarity_used, final_score)
    ON 
        p.product_id = t.product_id;
    """
    
    await db.execute(text(create_view_query))
    await db.commit()

async def execute_custom_query(db: AsyncSession, query):
    result = await db.execute(query)
    columns = result.keys()
    result = result.fetchall()
    return pd.DataFrame(result, columns=columns)

async def get_top_products_by_category(db: AsyncSession, filtered_df: pd.DataFrame, query=None):
    if query:
        # 정확히 일치하는 단어가 있는지 확인
        for keyword in FILTER_KEYWORDS:
            if check_exact_match(query, keyword):
                filtered_df = filtered_df[filtered_df['product_id'].isin(await get_filtered_product_ids(db, keyword))]
                break

    # Get top 10 product IDs based on final_score_semantic
    top_product_ids = filtered_df['product_id'].head(10).tolist()

    # Fetch product details from the database
    # result = await db.execute(select(Product).where(Product.product_id.in_(top_product_ids)))
    result = await db.execute(
        select(Product.product_id, Product.product_category, Product.product_name, Product.brand_name, Product.original_price, Product.final_price)
        .where(Product.product_id.in_(top_product_ids))
    )
    # products = result.all()
    columns = result.keys()
    top_products = result.all()
    return pd.DataFrame(top_products, columns=columns)

# 최종 결합 함수
async def get_final_recommendations(db: AsyncSession, user_vector, query_sentence, category=None):
    # 모델 초기화
    # model = SentenceTransformer('bespin-global/klue-sroberta-base-continue-learning-by-mnr')
    
    # 1. final_scores 계산
    final_scores_df = await calculate_final_scores(db, user_vector)
    
    # 2. final_scores_df에서 final_score >= 0인 데이터 필터링
    filtered_df = final_scores_df[final_scores_df['final_score'] >= 0]
    
    # 3. 필터링된 데이터에서 semantic search 수행
    filtered_product_ids = tuple(filtered_df['product_id'].tolist())
    top_products = await get_top_products_by_similarity(db, query_sentence, alpha=1.0, beta=1.0, gamma=1.5, top_n=len(filtered_product_ids))
    
    # print(filtered_df)
    # print(top_products)
    # 4. 결과를 결합
    merged_df = pd.merge(filtered_df, top_products, on='product_id', suffixes=('_recommendation', '_semantic'))
    merged_df = merged_df.sort_values(by='final_score_semantic', ascending=False)
    
    return merged_df


# 필터링해야 할 단어 목록
FILTER_KEYWORDS = ['크림', '에센스', '폼 클렌저', '미스트', '오일', '필링', '선크림', '토너', '클렌징 워터', '로션']

def check_exact_match(query, keyword):
    # 정규 표현식을 사용하여 정확히 일치하는 단어가 있는지 확인
    pattern = r'\b' + re.escape(keyword) + r'\b'
    return bool(re.search(pattern, query))

async def get_filtered_product_ids(db: AsyncSession, keyword):
    query = """
    SELECT product_id FROM product WHERE product_category = '%s';
    """ %(keyword)
    result = await db.execute(text(query))
    result = result.fetchall()
    return [row[0] for row in result]

async def execute_custom_query(db: AsyncSession, query):
    result = await db.execute(query)
    columns = result.keys()
    result = result.fetchall()
    return pd.DataFrame(result, columns=columns)


if __name__ == "__main__":

    # 데이터베이스 연결 설정
    conn = psycopg2.connect(
    database='', user='postgres', password='', host='localhost', port='5432'
    )

    cursor = conn.cursor()

    # 예시 실행
    query_sentence = "아빠한테 선물하기 좋은 토너"
    top_products = get_top_products_by_similarity(query_sentence, alpha=1.0, beta=1.0, gamma=1.5, top_n=10)
    # print(top_products)

    # 결과를 뷰로 생성
    create_view_from_df(top_products, 'top_product_view')

    user_query = "SELECT product_id, product_name FROM top_product_view;"
    result = execute_custom_query(user_query)
    # print(result)

    # 데이터베이스 연결 종료
    cursor.close()
    conn.close()
