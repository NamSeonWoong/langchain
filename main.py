"""
FastAPI 메인 애플리케이션
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import chat, rag

# FastAPI 앱 초기화
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="LangChain과 Ollama를 활용한 RAG 시스템"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(rag.router, prefix="/api/rag", tags=["RAG"])


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "LangChain RAG API에 오신 것을 환영합니다!",
        "version": settings.APP_VERSION,
        "endpoints": {
            "chat": "/api/chat/query",
            "rag_upload": "/api/rag/upload",
            "rag_query": "/api/rag/query",
            "rag_documents": "/api/rag/documents"
        }
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "ollama_url": settings.OLLAMA_BASE_URL,
        "model": settings.OLLAMA_MODEL
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

