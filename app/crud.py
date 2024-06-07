from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from . import models, schemas
import ast


# CRUD functions for Reviewer
async def get_reviewer(db: AsyncSession, reviewer_id: int):
    result = await db.execute(
        select(models.Reviewer).where(models.Reviewer.reviewer_id == reviewer_id)
    )
    return result.scalars().first()


async def get_reviewers(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Reviewer).offset(skip).limit(limit))
    return result.scalars().all()


async def create_reviewer(db: AsyncSession, reviewer: schemas.ReviewerCreate):
    db_reviewer = models.Reviewer(**reviewer.dict())
    db.add(db_reviewer)
    await db.commit()
    await db.refresh(db_reviewer)
    return db_reviewer


async def update_reviewer(
    db: AsyncSession, reviewer_id: int, reviewer_update: schemas.ReviewerCreate
):
    db_reviewer = await get_reviewer(db, reviewer_id)
    if not db_reviewer:
        return None
    for key, value in reviewer_update.dict().items():
        setattr(db_reviewer, key, value)
    await db.commit()
    await db.refresh(db_reviewer)
    return db_reviewer


async def delete_reviewer(db: AsyncSession, reviewer_id: int):
    db_reviewer = await get_reviewer(db, reviewer_id)
    if not db_reviewer:
        return None
    await db.delete(db_reviewer)
    await db.commit()
    return db_reviewer


# CRUD functions for Product
async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(models.Product).where(models.Product.product_id == product_id)
    )
    db_product = result.scalars().first()
    db_product.product_name_embedding = ast.literal_eval(
        db_product.product_name_embedding
    )

    return db_product


async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Product).offset(skip).limit(limit))
    db_products = result.scalars().all()
    for db_product in db_products:
        db_product.product_name_embedding = ast.literal_eval(
            db_product.product_name_embedding
        )
    return db_products


async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def update_product(
    db: AsyncSession, product_id: int, product_update: schemas.ProductCreate
):
    db_product = await get_product(db, product_id)
    if not db_product:
        return None
    for key, value in product_update.dict().items():
        setattr(db_product, key, value)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def delete_product(db: AsyncSession, product_id: int):
    db_product = await get_product(db, product_id)
    if not db_product:
        return None
    await db.delete(db_product)
    await db.commit()
    return db_product


# CRUD functions for Review
async def get_review(db: AsyncSession, review_id: int):
    result = await db.execute(
        select(models.Review).where(models.Review.review_id == review_id)
    )
    db_review = result.scalars().first()
    if db_review:
        db_review.review_content_embedding = ast.literal_eval(
            db_review.review_content_embedding
        )
    return db_review


async def get_reviews(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Review).offset(skip).limit(limit))
    db_reviews = result.scalars().all()

    for db_review in db_reviews:
        db_review.review_content_embedding = ast.literal_eval(
            db_review.review_content_embedding
        )

    return db_reviews


async def create_review(db: AsyncSession, review: schemas.ReviewCreate):
    db_review = models.Review(**review.dict())
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review


async def update_review(
    db: AsyncSession, review_id: int, review_update: schemas.ReviewCreate
):
    db_review = await get_review(db, review_id)
    if not db_review:
        return None
    for key, value in review_update.dict().items():
        setattr(db_review, key, value)
    await db.commit()
    await db.refresh(db_review)
    return db_review


async def delete_review(db: AsyncSession, review_id: int):
    db_review = await get_review(db, review_id)
    if not db_review:
        return None
    await db.delete(db_review)
    await db.commit()
    return db_review
