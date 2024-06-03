import psycopg2
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# 데이터베이스 연결 설정
conn = psycopg2.connect(
   database='', user='postgres', password='', host='localhost', port='5432'
)

cursor = conn.cursor()

# 요청 문장에 대한 제품 유사도 계산 함수
def get_top_products_by_similarity(query, alpha=1.0, beta=1.0, gamma=1.5, top_n=None):
    # 쿼리를 임베딩 벡터로 변환
    query_embedding = model.encode([query])[0].tolist()

    # product_similarities 테이블이 존재하면 삭제
    cursor.execute("DROP TABLE IF EXISTS product_similarities")

    # 제품명 임베딩과의 유사도 계산
    product_name_similarities_query = """
    CREATE TABLE product_similarities AS
    WITH query_embedding AS (
        SELECT %s::vector AS embedding
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
    """
    cursor.execute(product_name_similarities_query, (query_embedding,))
    conn.commit()

    cursor.execute("SELECT * FROM product_similarities")
    product_name_similarities = cursor.fetchall()

    # 리뷰 임베딩과의 유사도 계산 및 제품별 평균 유사도 계산
    review_similarities_query = """
    WITH query_embedding AS (
        SELECT %s::vector AS embedding
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
    """
    cursor.execute(review_similarities_query, (query_embedding, alpha, beta, gamma, gamma, gamma, alpha, beta, alpha + beta, top_n))
    final_scores = cursor.fetchall()

    # 결과 정리 및 출력
    result_df = pd.DataFrame(final_scores, columns=['product_id', 'name_similarity', 'review_count', 'used_count', 'avg_similarity', 'avg_similarity_used', 'final_score'])
    
    return result_df

def create_view_from_df(df, view_name):
    df_tuples = df.itertuples(index=False, name=None)
    values = ', '.join(cursor.mogrify('(%s,%s,%s,%s,%s,%s,%s)', row).decode('utf-8') for row in df_tuples)
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
    
    cursor.execute(create_view_query)
    conn.commit()

def execute_custom_query(query):
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])

# 모델 초기화
# model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
model = SentenceTransformer('bespin-global/klue-sroberta-base-continue-learning-by-mnr')

if __name__ == "__main__":
    # 예시 실행
    query_sentence = "아빠한테 선물하기 좋은 토너"
    top_products = get_top_products_by_similarity(query_sentence, alpha=1.0, beta=1.0, gamma=1.5, top_n=10)
    # print(top_products)

    # 결과를 뷰로 생성
    create_view_from_df(top_products, 'top_product_view')

    user_query = "SELECT product_id, product_name FROM top_product_view;"
    result = execute_custom_query(user_query)
    print(result)

    # 데이터베이스 연결 종료
    cursor.close()
    conn.close()
