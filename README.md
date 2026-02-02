# Langfuse Tutorial - 사전 준비 작업

Langfuse 통합 전 베이스라인 챗봇 애플리케이션입니다.

## 프로젝트 구조

```
langfuse-tutorial/
│   main.py              # FastAPI 백엔드
│   app.py              # Streamlit 프론트엔드
├── docs/
│   └── job_posting.txt     # 샘플 채용 공고 문서
└── .env                    # 환경 변수 (직접 생성)
└── requirements.txt     # 의존성
```

## 설치 및 실행

### 1. 환경 변수 설정

`.env.example`을 `.env`로 복사하고 OpenAI API 키를 입력합니다:

```bash
cp .env.example .env
```

`.env` 파일 수정:
```
OPENAI_API_KEY=your-actual-api-key-here
```

### 2. 의존성 설치
```bash
#의존성 설치
pip install -r requirements.txt

```

### 3. 백엔드 실행

```bash

# 서버 실행
python main.py
```

백엔드 서버가 `http://localhost:8000`에서 실행됩니다.

### 3. 프론트엔드 실행 (새 터미널)

```bash

# Streamlit 앱 실행
streamlit run app.py
```

프론트엔드가 `http://localhost:8501`에서 실행됩니다.

## API 문서

백엔드 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 주요 기능

- OpenAI GPT-3.5-turbo를 사용한 채팅
- 채용 공고 문서 기반 질의응답
- 토큰 사용량 추적
- 대화 히스토리 관리

## 다음 단계

이 베이스라인 프로젝트에 Langfuse를 통합하여:
- LLM 호출 추적
- 토큰 사용량 분석
- 프롬프트 성능 모니터링
- 사용자 피드백 수집

등의 기능을 추가할 예정입니다.