"""
LLM 및 임베딩 모델 설정
"""
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from config import settings


def get_llm():
    """
    Ollama LLM 인스턴스 반환
    
    Returns:
        Ollama: 설정된 Ollama LLM 인스턴스
    """
    llm = Ollama(
        base_url=settings.OLLAMA_BASE_URL,
        model=settings.OLLAMA_MODEL,
        temperature=settings.TEMPERATURE,
        num_predict=settings.MAX_TOKENS,
    )
    return llm


def get_embeddings():
    """
    Ollama 임베딩 모델 인스턴스 반환
    
    Returns:
        OllamaEmbeddings: 설정된 임베딩 모델 인스턴스
    """
    embeddings = OllamaEmbeddings(
        base_url=settings.OLLAMA_BASE_URL,
        model=settings.OLLAMA_EMBEDDING_MODEL,
    )
    return embeddings


def test_llm_connection():
    """
    LLM 연결 테스트
    
    Returns:
        dict: 테스트 결과
    """
    try:
        llm = get_llm()
        response = llm.invoke("안녕하세요!")
        return {
            "status": "success",
            "message": "LLM 연결 성공",
            "response": response
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"LLM 연결 실패: {str(e)}"
        }


def test_embeddings_connection():
    """
    임베딩 모델 연결 테스트
    
    Returns:
        dict: 테스트 결과
    """
    try:
        embeddings = get_embeddings()
        test_embedding = embeddings.embed_query("테스트")
        return {
            "status": "success",
            "message": "임베딩 모델 연결 성공",
            "embedding_dimension": len(test_embedding)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"임베딩 모델 연결 실패: {str(e)}"
        }

