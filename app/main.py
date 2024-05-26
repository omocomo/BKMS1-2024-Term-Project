from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from . import crud, schemas
from .database import engine, Base, get_db
from typing import List

app = FastAPI()

# 데이터베이스 초기화
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 간단한 테스트 엔드포인트 추가
@app.get("/test_db_connection/")
async def test_db_connection(db: AsyncSession = Depends(get_db)):
    try:
        # 간단한 쿼리 실행
        result = await db.execute("SELECT 1")
        return {"status": "success", "result": result.scalar()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


