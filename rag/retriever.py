"""
검색기 - 벡터 스토어를 활용한 문서 검색
"""
from typing import List
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from rag.vector_store import vector_store_manager
from config import settings


class DocumentRetriever:
    """문서 검색 클래스"""
    
    def __init__(self):
        """초기화"""
        self.vector_store_manager = vector_store_manager
    
    def get_retriever(self, k: int = None) -> BaseRetriever:
        """
        LangChain Retriever 반환
        
        Args:
            k: 검색할 문서 개수
            
        Returns:
            BaseRetriever: 검색기 인스턴스
        """
        k = k or settings.TOP_K
        vectorstore = self.vector_store_manager.load_vectorstore()
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
        return retriever
    
    def retrieve_documents(self, query: str, k: int = None) -> List[Document]:
        """
        쿼리에 대한 관련 문서 검색
        
        Args:
            query: 검색 쿼리
            k: 검색할 문서 개수
            
        Returns:
            List[Document]: 검색된 문서 리스트
        """
        k = k or settings.TOP_K
        documents = self.vector_store_manager.search(query, k=k)
        return documents
    
    def retrieve_with_scores(self, query: str, k: int = None) -> List[tuple]:
        """
        점수와 함께 문서 검색
        
        Args:
            query: 검색 쿼리
            k: 검색할 문서 개수
            
        Returns:
            List[tuple]: (문서, 점수) 튜플 리스트
        """
        k = k or settings.TOP_K
        results = self.vector_store_manager.search_with_score(query, k=k)
        return results
    
    def format_documents(self, documents: List[Document]) -> str:
        """
        문서 리스트를 텍스트로 포맷팅
        
        Args:
            documents: 문서 리스트
            
        Returns:
            str: 포맷팅된 텍스트
        """
        formatted = "\n\n".join([doc.page_content for doc in documents])
        return formatted


# 전역 인스턴스
document_retriever = DocumentRetriever()

