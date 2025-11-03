"""
문서 로더 - 다양한 형식의 문서를 로드하고 전처리
"""
import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    DirectoryLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import settings


class DocumentProcessor:
    """문서 처리 클래스"""
    
    def __init__(self):
        """초기화"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_pdf(self, file_path: str) -> List[Document]:
        """
        PDF 파일 로드
        
        Args:
            file_path: PDF 파일 경로
            
        Returns:
            List[Document]: 로드된 문서 리스트
        """
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents
    
    def load_text(self, file_path: str) -> List[Document]:
        """
        텍스트 파일 로드
        
        Args:
            file_path: 텍스트 파일 경로
            
        Returns:
            List[Document]: 로드된 문서 리스트
        """
        loader = TextLoader(file_path, encoding='utf-8')
        documents = loader.load()
        return documents
    
    def load_directory(self, directory_path: str) -> List[Document]:
        """
        디렉토리 내 모든 문서 로드
        
        Args:
            directory_path: 디렉토리 경로
            
        Returns:
            List[Document]: 로드된 문서 리스트
        """
        documents = []
        
        # PDF 파일 로드
        pdf_loader = DirectoryLoader(
            directory_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        pdf_docs = pdf_loader.load()
        documents.extend(pdf_docs)
        
        # 텍스트 파일 로드
        txt_loader = DirectoryLoader(
            directory_path,
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={'encoding': 'utf-8'}
        )
        txt_docs = txt_loader.load()
        documents.extend(txt_docs)
        
        return documents
    
    def load_document(self, file_path: str) -> List[Document]:
        """
        파일 확장자에 따라 자동으로 적절한 로더 선택
        
        Args:
            file_path: 파일 경로
            
        Returns:
            List[Document]: 로드된 문서 리스트
        """
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext == '.pdf':
            return self.load_pdf(file_path)
        elif ext in ['.txt', '.md']:
            return self.load_text(file_path)
        else:
            raise ValueError(f"지원하지 않는 파일 형식입니다: {ext}")
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        문서를 청크로 분할
        
        Args:
            documents: 분할할 문서 리스트
            
        Returns:
            List[Document]: 분할된 문서 청크 리스트
        """
        chunks = self.text_splitter.split_documents(documents)
        return chunks
    
    def process_document(self, file_path: str) -> List[Document]:
        """
        문서 로드 및 분할 통합 처리
        
        Args:
            file_path: 파일 경로
            
        Returns:
            List[Document]: 처리된 문서 청크 리스트
        """
        # 문서 로드
        documents = self.load_document(file_path)
        
        # 문서 분할
        chunks = self.split_documents(documents)
        
        return chunks


# 전역 인스턴스
document_processor = DocumentProcessor()

