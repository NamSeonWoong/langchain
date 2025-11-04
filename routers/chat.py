"""
채팅 라우터 - 일반 대화 API
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from models.llm_setup import get_llm, test_llm_connection

router = APIRouter()


class Message(BaseModel):
    """메시지 모델"""
    role: str  # "user" 또는 "assistant"
    content: str


class ChatRequest(BaseModel):
    """채팅 요청 모델"""
    message: str
    temperature: float = 0.7
    history: Optional[List[Message]] = []


class ChatResponse(BaseModel):
    """채팅 응답 모델"""
    response: str


@router.post("/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest):
    """
    일반 채팅 질의 (대화 메모리 포함)
    
    Args:
        request: 채팅 요청 (메시지, 온도, 히스토리)
        
    Returns:
        ChatResponse: LLM 응답
    """
    try:
        llm = get_llm()
        
        # 온도 설정이 기본값과 다른 경우 업데이트
        if request.temperature != 0.7:
            llm.temperature = request.temperature
        
        # 대화 히스토리가 있으면 컨텍스트 구성
        if request.history and len(request.history) > 0:
            # 이전 대화를 포함한 프롬프트 구성
            context = "이전 대화:\n"
            for msg in request.history[-6:]:  # 최근 6개 메시지만 (3턴)
                if msg.role == "user":
                    context += f"사용자: {msg.content}\n"
                else:
                    context += f"AI: {msg.content}\n"
            
            context += f"\n현재 질문: {request.message}\n\n"
            context += "위 대화 맥락을 고려하여 현재 질문에 답변해주세요:"
            
            full_prompt = context
        else:
            full_prompt = request.message
        
        # LLM 호출
        response = llm.invoke(full_prompt)
        
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

