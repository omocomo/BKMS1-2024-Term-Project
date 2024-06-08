from sqlalchemy.future import select
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Review, Product, Reviewer
from datetime import datetime
import pandas as pd

async def get_reviews_by_product_and_keyword(db: AsyncSession, product_name: str, keyword: str):
    print(product_name, keyword)
    result = await db.execute(select(Review).where(Review.product_name.like(f'%{product_name}%{keyword}%')))
    result_reviews = result.scalars().all()
    # 리뷰 데이터를 DataFrame으로 변환
    review_data = [
        {
            "product_name": review.product_name,
            "reviewer_name": review.reviewer_name,
            "rating": review.rating,
            "used_over_one_month": review.used_over_one_month,
            "repurchase_intention": review.repurchase_intention,
            "skin_type_review": review.skin_type_review,
            "skin_concern_review": review.skin_concern_review,
            "irritation_level_review": review.irritation_level_review,
            "cleansing_power_review": review.cleansing_power_review,
            "spreadability_review": review.spreadability_review,
            "review_content": review.review_content,
            "review_date": review.review_date,
        }
        for review in result_reviews
    ]
    result_df = pd.DataFrame(review_data)
    return result_df

async def get_reviews_by_rating(db: AsyncSession, product_name: str):
    result = await db.execute(select(Review).where((Review.product_name.like(f'%{product_name}%')) & (Review.rating != 5)))
    result_reviews = result.scalars().all()
    # 리뷰 데이터를 DataFrame으로 변환
    review_data = [
        {
            "product_name": review.product_name,
            "reviewer_name": review.reviewer_name,
            "rating": review.rating,
            "used_over_one_month": review.used_over_one_month,
            "repurchase_intention": review.repurchase_intention,
            "skin_type_review": review.skin_type_review,
            "skin_concern_review": review.skin_concern_review,
            "irritation_level_review": review.irritation_level_review,
            "cleansing_power_review": review.cleansing_power_review,
            "spreadability_review": review.spreadability_review,
            "review_content": review.review_content,
            "review_date": review.review_date,
        }
        for review in result_reviews
    ]
    result_df = pd.DataFrame(review_data)
    return result_df

async def get_reviews_by_date_range(db: AsyncSession, start_date: datetime, end_date: datetime):
    result = await db.execute(select(Review).where(Review.created_at.between(start_date, end_date)))
    result_reviews = result.scalars().all()
    # 리뷰 데이터를 DataFrame으로 변환
    review_data = [
        {
            "product_name": review.product_name,
            "reviewer_name": review.reviewer_name,
            "rating": review.rating,
            "used_over_one_month": review.used_over_one_month,
            "repurchase_intention": review.repurchase_intention,
            "skin_type_review": review.skin_type_review,
            "skin_concern_review": review.skin_concern_review,
            "irritation_level_review": review.irritation_level_review,
            "cleansing_power_review": review.cleansing_power_review,
            "spreadability_review": review.spreadability_review,
            "review_content": review.review_content,
            "review_date": review.review_date,
        }
        for review in result_reviews
    ]
    result_df = pd.DataFrame(review_data)
    return result_df

async def get_review_count_and_average_star_by_product(db: AsyncSession):
    result = await db.execute(
        select(
            Review.product_id,
            func.count(Review.review_id).label('review_count'),
            func.avg(Review.rating).label('average_star')
        ).group_by(Review.product_id)
    )
    result_reviews = result.scalars().all()
    # 리뷰 데이터를 DataFrame으로 변환
    review_data = [
        {
            "product_name": review.product_name,
            "reviewer_name": review.reviewer_name,
            "rating": review.rating,
            "used_over_one_month": review.used_over_one_month,
            "repurchase_intention": review.repurchase_intention,
            "skin_type_review": review.skin_type_review,
            "skin_concern_review": review.skin_concern_review,
            "irritation_level_review": review.irritation_level_review,
            "cleansing_power_review": review.cleansing_power_review,
            "spreadability_review": review.spreadability_review,
            "review_content": review.review_content,
            "review_date": review.review_date,
        }
        for review in result_reviews
    ]
    result_df = pd.DataFrame(review_data)
    return result_df

async def get_reviews_by_skin_type(db: AsyncSession, skin_type: str):
    result = await db.execute(
        select(Review, Product, Reviewer)
        .join(Product, Review.product_id == Product.product_id)
        .join(Reviewer, Review.reviewer_id == Reviewer.reviewer_id)
        .where(Review.skin_type == skin_type)
    )
    result_reviews = result.scalars().all()
    # 리뷰 데이터를 DataFrame으로 변환
    review_data = [
        {
            "product_name": review.product_name,
            "reviewer_name": review.reviewer_name,
            "rating": review.rating,
            "used_over_one_month": review.used_over_one_month,
            "repurchase_intention": review.repurchase_intention,
            "skin_type_review": review.skin_type_review,
            "skin_concern_review": review.skin_concern_review,
            "irritation_level_review": review.irritation_level_review,
            "cleansing_power_review": review.cleansing_power_review,
            "spreadability_review": review.spreadability_review,
            "review_content": review.review_content,
            "review_date": review.review_date,
        }
        for review in result_reviews
    ]
    result_df = pd.DataFrame(review_data)
    return result_df

async def get_similar_reviews(db: AsyncSession, review_content_embedding):
    result = await db.execute(
        select(Review, 1 - func.cube_distance(Review.review_content_embedding, review_content_embedding).label('similarity_score'))
        .where(1 - func.cube_distance(Review.review_content_embedding, review_content_embedding) > 0.8)
    )
    result_reviews = result.scalars().all()
    # 리뷰 데이터를 DataFrame으로 변환
    review_data = [
        {
            "product_name": review.product_name,
            "reviewer_name": review.reviewer_name,
            "rating": review.rating,
            "used_over_one_month": review.used_over_one_month,
            "repurchase_intention": review.repurchase_intention,
            "skin_type_review": review.skin_type_review,
            "skin_concern_review": review.skin_concern_review,
            "irritation_level_review": review.irritation_level_review,
            "cleansing_power_review": review.cleansing_power_review,
            "spreadability_review": review.spreadability_review,
            "review_content": review.review_content,
            "review_date": review.review_date,
        }
        for review in result_reviews
    ]
    result_df = pd.DataFrame(review_data)
    return result_df

async def get_brand_review_ratios(db: AsyncSession, brand_name: str):
    result = await db.execute(
        select(
            Product.brand_name,
            func.count(Review.review_id).label('total_reviews'),
            func.sum(func.case([(Review.used_over_one_month, 1)], else_=0)) / func.count(Review.review_id).label('used_over_one_month_ratio'),
            func.sum(func.case([(Review.repurchase_intention, 1)], else_=0)) / func.count(Review.review_id).label('repurchase_intention_ratio')
        ).join(Product, Review.product_id == Product.product_id)
        .where(Product.brand_name == brand_name)
        .group_by(Product.brand_name)
    )
    result_reviews = result.scalars().all()
    # 리뷰 데이터를 DataFrame으로 변환
    review_data = [
        {
            "product_name": review.product_name,
            "reviewer_name": review.reviewer_name,
            "rating": review.rating,
            "used_over_one_month": review.used_over_one_month,
            "repurchase_intention": review.repurchase_intention,
            "skin_type_review": review.skin_type_review,
            "skin_concern_review": review.skin_concern_review,
            "irritation_level_review": review.irritation_level_review,
            "cleansing_power_review": review.cleansing_power_review,
            "spreadability_review": review.spreadability_review,
            "review_content": review.review_content,
            "review_date": review.review_date,
        }
        for review in result_reviews
    ]
    result_df = pd.DataFrame(review_data)
    return result_df