from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, schemas, recsys
from .database import engine, Base, get_db
from typing import List
from sqlalchemy import text

app = FastAPI()


# 데이터베이스 초기화
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # 시퀀스 값을 최대값보다 높은 값으로 설정
        await conn.execute(
            text(
                """
            DO $$
            DECLARE
                rec RECORD;
            BEGIN
                FOR rec IN (SELECT c.relname AS sequence_name, t.relname AS table_name, a.attname AS column_name
                            FROM pg_class c
                            JOIN pg_depend d ON d.objid = c.oid
                            JOIN pg_class t ON t.oid = d.refobjid
                            JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = d.refobjsubid
                            WHERE c.relkind = 'S') LOOP
                    EXECUTE 'SELECT setval(''' || rec.sequence_name || ''', COALESCE((SELECT MAX(' || rec.column_name || ') + 1 FROM ' || rec.table_name || '), 1), false)';
                END LOOP;
            END
            $$;
            """
            )
        )
        # 트리거 함수 생성
        trigger_function_sql = """
        CREATE OR REPLACE FUNCTION update_product_review_stats()
        RETURNS TRIGGER AS $$
        BEGIN
            -- 제품 평점 및 리뷰 수 업데이트
            UPDATE product
            SET number_of_reviews = number_of_reviews + 1,
                review_rating = CEIL((SELECT AVG(rating) FROM review WHERE product_id = NEW.product_id))
            WHERE product_id = NEW.product_id;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
        await conn.execute(text(trigger_function_sql))

        # 기존 트리거 삭제
        await conn.execute(
            text("DROP TRIGGER IF EXISTS review_insert_trigger ON review")
        )

        # 트리거 생성
        trigger_sql = """
        CREATE TRIGGER review_insert_trigger
        AFTER INSERT ON review
        FOR EACH ROW
        EXECUTE FUNCTION update_product_review_stats();
        """
        await conn.execute(text(trigger_sql))


# 간단한 테스트 엔드포인트 추가
@app.get("/test_db_connection/")
async def test_db_connection(db: AsyncSession = Depends(get_db)):
    try:
        # 간단한 쿼리 실행
        result = await db.execute("SELECT 1")
        return {"status": "success", "result": result.scalar()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Reviewer CRUD endpoints
@app.post("/reviewers/", response_model=schemas.Reviewer)
async def create_reviewer(
    reviewer: schemas.ReviewerCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_reviewer(db=db, reviewer=reviewer)


@app.get("/reviewers/{reviewer_id}", response_model=schemas.Reviewer)
async def read_reviewer(reviewer_id: int, db: AsyncSession = Depends(get_db)):
    db_reviewer = await crud.get_reviewer(db, reviewer_id=reviewer_id)
    if db_reviewer is None:
        raise HTTPException(status_code=404, detail="Reviewer not found")
    return db_reviewer


@app.get("/reviewers/", response_model=List[schemas.Reviewer])
async def read_reviewers(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    reviewers = await crud.get_reviewers(db, skip=skip, limit=limit)
    return reviewers


@app.put("/reviewers/{reviewer_id}", response_model=schemas.Reviewer)
async def update_reviewer(
    reviewer_id: int,
    reviewer: schemas.ReviewerCreate,
    db: AsyncSession = Depends(get_db),
):
    db_reviewer = await crud.update_reviewer(
        db, reviewer_id=reviewer_id, reviewer_update=reviewer
    )
    if db_reviewer is None:
        raise HTTPException(status_code=404, detail="Reviewer not found")
    return db_reviewer


@app.delete("/reviewers/{reviewer_id}", response_model=schemas.Reviewer)
async def delete_reviewer(reviewer_id: int, db: AsyncSession = Depends(get_db)):
    db_reviewer = await crud.delete_reviewer(db, reviewer_id=reviewer_id)
    if db_reviewer is None:
        raise HTTPException(status_code=404, detail="Reviewer not found")
    return db_reviewer


# Product CRUD endpoints
@app.post("/products/", response_model=schemas.Product)
async def create_product(
    product: schemas.ProductCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_product(db=db, product=product)


@app.get("/products/{product_id}", response_model=schemas.Product)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    db_product = await crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.get("/products/", response_model=List[schemas.Product])
async def read_products(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    products = await crud.get_products(db, skip=skip, limit=limit)
    return products


@app.put("/products/{product_id}", response_model=schemas.Product)
async def update_product(
    product_id: int, product: schemas.ProductCreate, db: AsyncSession = Depends(get_db)
):
    db_product = await crud.update_product(
        db, product_id=product_id, product_update=product
    )
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.delete("/products/{product_id}", response_model=schemas.Product)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    db_product = await crud.delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


# Review CRUD endpoints
@app.post("/reviews/", response_model=schemas.Review)
async def create_review(
    review: schemas.ReviewCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_review(db=db, review=review)


@app.get("/reviews/{review_id}", response_model=schemas.Review)
async def read_review(review_id: int, db: AsyncSession = Depends(get_db)):
    db_review = await crud.get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review


@app.get("/reviews/", response_model=List[schemas.Review])
async def read_reviews(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    reviews = await crud.get_reviews(db, skip=skip, limit=limit)
    return reviews


@app.put("/reviews/{review_id}", response_model=schemas.Review)
async def update_review(
    review_id: int, review: schemas.ReviewCreate, db: AsyncSession = Depends(get_db)
):
    db_review = await crud.update_review(db, review_id=review_id, review_update=review)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review


@app.delete("/reviews/{review_id}", response_model=schemas.Review)
async def delete_review(review_id: int, db: AsyncSession = Depends(get_db)):
    db_review = await crud.delete_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review


@app.get("/recsys/{query}")
async def recsys_product(query: str):
    top_products = recsys.get_top_products_by_similarity(
        query, alpha=1.0, beta=1.0, gamma=1.5, top_n=10
    )
    recsys.create_view_from_df(top_products, "top_product_view")
    recommend = recsys.execute_custom_query(
        "SELECT product_id, product_name FROM top_product_view;"
    )
    return recommend.to_dict(orient="records")
