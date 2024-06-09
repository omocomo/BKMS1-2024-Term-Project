## 개요
본 프로젝트에서는 올리브영의 데이터를 활용하여 기본적인 데이터베이스를 만들었다. 리뷰와 상품정보, 그리고 유저 정보 데이터를 수집하여 데이터베이스를 만들고, 새로운 입력과 업데이트, 삭제를 처리할 수 있도록 만들었다. 또한 join, transaction, trigger 등의 쿼리도 문제없이 동작할 수 있는 backend 데이터베이스를 설계했다. 그리고, 더 나아가서 사용자들이 남겨두었던 리뷰를 임베딩을 통해 활용할 수 있는 방법에 대해 고민해보고 활용하였다. 이 임베딩들을 이용해 Hybrid Recommendation System을 개발하였다. 구체적으로는 Semantic Search, User-Based Collaborative Filtering (CF), Content-Based Filtering (CBF)를 할 수 있도록 해주어 올리브영 웹페이지의 사용자 경험을 향상할 수 있는 방안을 제시한다.

## 프로젝트 구조 
```
BKMS1-2024-Term-Project
├── app
│   ├── images
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── recsys.py
│   ├── review_search.py
│   ├── schemas.py
│   └── streamlit.py
├── .gitignore
├── .gitmessage
├── README.md
├── csv_upload.py
└── requirements.txt
```
## How to Run

### 사전준비

- 가상환경 만들기 (Conda, venv whatever you want)
- Run postgresql server
- root folder에 .env 만들어서 주소 넣어놓기
  - .env example : `DATABASE_URL=postgresql+asyncpg://postgres:mypassword@localhost:5432/mydatabase`
  - format : `[user[:password]@][netloc][:port][/dbname]`
- `pip install -r requirements.txt`

### postgresql 에서 pgvector 설치

`psql -U postgres -c "CREATE EXTENSION IF NOT EXISTS vector;"`

### Run code (root folder)
`uvicorn app.main:app --reload` ## Backend                   
`streamlit run app/streamlit.py` ## Frontend
