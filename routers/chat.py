"""
채팅 라우터 - 일반 대화 API
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.llm_setup import get_llm, test_llm_connection

router = APIRouter()


class ChatRequest(BaseModel):
    """채팅 요청 모델"""
    message: str
    temperature: float = 0.7


class ChatResponse(BaseModel):
    """채팅 응답 모델"""
    response: str


@router.post("/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest):
    """
    일반 채팅 질의
    
    Args:
        request: 채팅 요청 (메시지, 온도)
        
    Returns:
        ChatResponse: LLM 응답
    """
    try:
        llm = get_llm()
        
        # 온도 설정이 기본값과 다른 경우 업데이트
        if request.temperature != 0.7:
            llm.temperature = request.temperature
        
        # LLM 호출
        response = llm.invoke(request.message)
        
        return ChatResponse(response=response)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"채팅 처리 중 오류 발생: {str(e)}"
        )


@router.get("/test")
async def test_connection():
    """
    LLM 연결 테스트
    
    Returns:
        dict: 테스트 결과
    """
    try:
        result = test_llm_connection()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"연결 테스트 실패: {str(e)}"
        )

