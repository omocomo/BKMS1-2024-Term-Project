## 사전준비

가상환경 만들기

postgresql 로컬에 켜놓기
.env 만들어서 주소 넣어놓기

### postgresql 에서 pgvector 설치

psql -U postgres -c "CREATE EXTENSION IF NOT EXISTS vector;"

## 실행

uvicorn app.main:app --reload ## root folder에서 실행     
streamlit run app/streamlit.py ## root folder에서 실행 

