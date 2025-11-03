"""
설정 파일 - Ollama 및 애플리케이션 설정
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # Ollama 설정
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1"  # 사용할 LLM 모델
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"  # 임베딩 모델
    
    # 애플리케이션 설정
    APP_NAME: str = "LangChain RAG API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # RAG 설정
    CHUNK_SIZE: int = 1000  # 문서 청크 크기
    CHUNK_OVERLAP: int = 200  # 청크 오버랩
    TOP_K: int = 4  # 검색할 문서 개수
    
    # 벡터 스토어 설정
    VECTOR_STORE_PATH: str = "./chroma_db"
    COLLECTION_NAME: str = "documents"
    
    # 문서 저장 경로
    UPLOAD_DIR: str = "./data"
    
    # LLM 파라미터
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

