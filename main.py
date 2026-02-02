from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

# 환경 변수 로드
load_dotenv()

app = FastAPI(
    title="Langfuse Tutorial ChatBot API",
    description="간단한 채팅 API (Langfuse 통합 전)",
    version="0.1.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI 클라이언트 초기화
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 문서 로드
def load_document(doc_name: str = "job_posting.txt") -> str:
    """docs 폴더에서 문서를 로드합니다."""
    doc_path = Path(__file__).parent / "docs" / doc_name
    if doc_path.exists():
        with open(doc_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# 시스템 프롬프트
SYSTEM_PROMPT = """당신은 채용 공고 안내 챗봇입니다.
사용자의 질문에 친절하고 명확하게 답변해주세요.
제공된 채용 공고 정보를 참고하여 답변하되, 정보가 없는 경우 솔직히 모른다고 답변하세요."""

# 요청 모델
class ChatRequest(BaseModel):
    message: str
    use_document: bool = True

class ChatResponse(BaseModel):
    response: str
    model: str
    tokens_used: dict

@app.get("/")
async def root():
    """API 상태 확인"""
    return {
        "status": "running",
        "message": "Langfuse Tutorial ChatBot API",
        "version": "0.1.0"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """채팅 엔드포인트"""
    try:
        # 메시지 구성
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # 문서 컨텍스트 추가
        if request.use_document:
            doc_content = load_document()
            if doc_content:
                context_message = f"다음은 참고할 채용 공고 정보입니다:\n\n{doc_content}"
                messages.append({"role": "system", "content": context_message})
        
        # 사용자 메시지 추가
        messages.append({"role": "user", "content": request.message})
        
        # OpenAI API 호출
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        # 응답 반환
        return ChatResponse(
            response=response.choices[0].message.content,
            model=response.model,
            tokens_used={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)