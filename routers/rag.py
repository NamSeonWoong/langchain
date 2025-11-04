"""
RAG 라우터 - 문서 기반 질의응답 API
"""
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from rag.document_loader import document_processor
from rag.vector_store import vector_store_manager
from chains.qa_chain import qa_chain_manager
from config import settings

router = APIRouter()


class RAGQueryRequest(BaseModel):
    """RAG 쿼리 요청 모델"""
    question: str
    top_k: int = 4


class RAGQueryResponse(BaseModel):
    """RAG 쿼리 응답 모델"""
    question: str
    answer: str
    source_documents: List[Dict[str, Any]]


class DocumentInfo(BaseModel):
    """문서 정보 모델"""
    filename: str
    size: int
    chunks: int


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    문서 업로드 및 벡터화
    
    Args:
        file: 업로드할 파일 (PDF, TXT, MD)
        
    Returns:
        dict: 업로드 결과
    """
    try:
        # 파일 확장자 확인
        filename = file.filename
        _, ext = os.path.splitext(filename)
        
        if ext.lower() not in ['.pdf', '.txt', '.md']:
            raise HTTPException(
                status_code=400,
                detail="지원하지 않는 파일 형식입니다. PDF, TXT, MD 파일만 가능합니다."
            )
        
        # 업로드 디렉토리 생성
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # 파일 저장
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 문서 처리 (로드 및 분할)
        chunks = document_processor.process_document(file_path)
        
        # 벡터 스토어에 추가
        vector_store_manager.add_documents(chunks)
        
        return {
            "status": "success",
            "message": "문서가 성공적으로 업로드되고 벡터화되었습니다.",
            "filename": filename,
            "chunks": len(chunks),
            "total_documents": vector_store_manager.get_collection_count()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"\n{'='*60}")
        print("문서 업로드 오류 발생!")
        print(f"{'='*60}")
        print(error_trace)
        print(f"{'='*60}\n")
        raise HTTPException(
            status_code=500,
            detail=f"문서 업로드 중 오류 발생: {str(e)}"
        )


@router.post("/query", response_model=RAGQueryResponse)
async def rag_query(request: RAGQueryRequest):
    """
    RAG 기반 질의응답
    
    Args:
        request: RAG 쿼리 요청
        
    Returns:
        RAGQueryResponse: 답변 및 소스 문서
    """
    try:
        # 벡터 스토어에 문서가 있는지 확인
        doc_count = vector_store_manager.get_collection_count()
        if doc_count == 0:
            raise HTTPException(
                status_code=400,
                detail="업로드된 문서가 없습니다. 먼저 문서를 업로드해주세요."
            )
        
        # QA 체인으로 질의응답
        result = qa_chain_manager.query(request.question)
        
        return RAGQueryResponse(
            question=result["question"],
            answer=result["answer"],
            source_documents=result["source_documents"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"질의응답 처리 중 오류 발생: {str(e)}"
        )


@router.get("/documents")
async def get_documents_info():
    """
    저장된 문서 정보 조회
    
    Returns:
        dict: 문서 정보
    """
    try:
        doc_count = vector_store_manager.get_collection_count()
        
        # data 디렉토리의 파일 목록
        uploaded_files = []
        if os.path.exists(settings.UPLOAD_DIR):
            for filename in os.listdir(settings.UPLOAD_DIR):
                file_path = os.path.join(settings.UPLOAD_DIR, filename)
                if os.path.isfile(file_path):
                    uploaded_files.append({
                        "filename": filename,
                        "size": os.path.getsize(file_path)
                    })
        
        return {
            "total_chunks": doc_count,
            "uploaded_files": uploaded_files,
            "collection_name": settings.COLLECTION_NAME
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"문서 정보 조회 중 오류 발생: {str(e)}"
        )


@router.delete("/documents")
async def delete_all_documents():
    """
    모든 문서 삭제
    
    Returns:
        dict: 삭제 결과
    """
    try:
        # 벡터 스토어 컬렉션 삭제
        vector_store_manager.delete_collection()
        
        return {
            "status": "success",
            "message": "모든 문서가 삭제되었습니다."
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"문서 삭제 중 오류 발생: {str(e)}"
        )

