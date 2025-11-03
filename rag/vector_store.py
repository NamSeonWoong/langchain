"""
벡터 스토어 관리 - ChromaDB를 사용한 벡터 데이터베이스
"""
from typing import List, Optional
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import Embeddings
from models.llm_setup import get_embeddings
from config import settings
import os


class VectorStoreManager:
    """벡터 스토어 관리 클래스"""
    
    def __init__(self, embeddings: Optional[Embeddings] = None):
        """
        초기화
        
        Args:
            embeddings: 임베딩 모델 (기본값: Ollama 임베딩)
        """
        self.embeddings = embeddings or get_embeddings()
        self.persist_directory = settings.VECTOR_STORE_PATH
        self.collection_name = settings.COLLECTION_NAME
        
        # 디렉토리 생성
        os.makedirs(self.persist_directory, exist_ok=True)
    
    def create_vectorstore(self, documents: List[Document]) -> Chroma:
        """
        새로운 벡터 스토어 생성
        
        Args:
            documents: 벡터화할 문서 리스트
            
        Returns:
            Chroma: 생성된 벡터 스토어
        """
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=self.collection_name
        )
        return vectorstore
    
    def load_vectorstore(self) -> Chroma:
        """
        기존 벡터 스토어 로드
        
        Returns:
            Chroma: 로드된 벡터 스토어
        """
        vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name=self.collection_name
        )
        return vectorstore
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        벡터 스토어에 문서 추가
        
        Args:
            documents: 추가할 문서 리스트
        """
        vectorstore = self.load_vectorstore()
        vectorstore.add_documents(documents)
    
    def search(self, query: str, k: int = None) -> List[Document]:
        """
        유사도 검색
        
        Args:
            query: 검색 쿼리
            k: 반환할 문서 개수
            
        Returns:
            List[Document]: 검색된 문서 리스트
        """
        k = k or settings.TOP_K
        vectorstore = self.load_vectorstore()
        results = vectorstore.similarity_search(query, k=k)
        return results
    
    def search_with_score(self, query: str, k: int = None) -> List[tuple]:
        """
        점수와 함께 유사도 검색
        
        Args:
            query: 검색 쿼리
            k: 반환할 문서 개수
            
        Returns:
            List[tuple]: (문서, 점수) 튜플 리스트
        """
        k = k or settings.TOP_K
        vectorstore = self.load_vectorstore()
        results = vectorstore.similarity_search_with_score(query, k=k)
        return results
    
    def delete_collection(self) -> None:
        """컬렉션 삭제"""
        vectorstore = self.load_vectorstore()
        vectorstore.delete_collection()
    
    def get_collection_count(self) -> int:
        """
        컬렉션 내 문서 개수 반환
        
        Returns:
            int: 문서 개수
        """
        try:
            vectorstore = self.load_vectorstore()
            # ChromaDB의 컬렉션에서 문서 개수 조회
            collection = vectorstore._collection
            return collection.count()
        except:
            return 0


# 전역 인스턴스
vector_store_manager = VectorStoreManager()

