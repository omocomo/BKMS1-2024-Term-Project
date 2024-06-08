from sqlalchemy.future import select
from sqlalchemy import func, case
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

async def get_reviews_by_rating(db: AsyncSession, product_id: int, rating: int):
    result = await db.execute(select(Review).where((Review.product_id==product_id) & (Review.rating==rating)))
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
    result = await db.execute(select(Review).where(Review.review_date.between(start_date, end_date)))
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

async def get_review_count_and_average_star_by_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.product_id==product_id))
    result = result.scalars().all()
    product_data = [
        {
            "product_name": product.product_name,
            "number_of_reviews": product.number_of_reviews,
            "review_5_star_ratio": product.review_5_star_ratio,
            "review_4_star_ratio": product.review_4_star_ratio,
            "review_3_star_ratio": product.review_3_star_ratio,
            "review_2_star_ratio": product.review_2_star_ratio,
            "review_1_star_ratio": product.review_1_star_ratio,
        }
        for product in result
    ]
    result_df = pd.DataFrame(product_data)
    return result_df

async def get_brand_review_ratios(db: AsyncSession, brand_name: str):
    result = await db.execute(
        select(
            Product.brand_name,
            func.count(Review.review_id).label('total_reviews'),
            (func.sum(case((Review.used_over_one_month == True, 1), else_=0)) / func.count(Review.review_id)).label('used_over_one_month_ratio'),
            (func.sum(case((Review.repurchase_intention == True, 1), else_=0)) / func.count(Review.review_id)).label('repurchase_intention_ratio')
        ).join(Product, Review.product_id == Product.product_id)
        .where(Product.brand_name == brand_name)
        .group_by(Product.brand_name)
    )
    result_reviews = result.fetchall()
    result_df = pd.DataFrame(result_reviews, columns=['brand_name', 'total_reviews', 'used_over_one_month_ratio', 'repurchase_intention_ratio'])
    return result_df