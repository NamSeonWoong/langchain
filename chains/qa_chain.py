"""
질의응답 체인 - RAG를 활용한 QA 시스템
"""
from typing import Dict, Any
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from models.llm_setup import get_llm
from rag.retriever import document_retriever


# RAG 프롬프트 템플릿
RAG_PROMPT_TEMPLATE = """다음 컨텍스트를 사용하여 질문에 답변해주세요.
컨텍스트에 답변이 없는 경우, 모르겠다고 솔직히 말해주세요. 답변을 지어내지 마세요.

컨텍스트:
{context}

질문: {question}

답변:"""


class QAChainManager:
    """질의응답 체인 관리 클래스"""
    
    def __init__(self):
        """초기화"""
        self.llm = get_llm()
        self.retriever = document_retriever.get_retriever()
        
        # 프롬프트 설정
        self.prompt = PromptTemplate(
            template=RAG_PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )
    
    def create_qa_chain(self) -> RetrievalQA:
        """
        RAG 기반 QA 체인 생성
        
        Returns:
            RetrievalQA: 질의응답 체인
        """
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={
                "prompt": self.prompt,
                "verbose": False
            }
        )
        return qa_chain
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        질문에 대한 답변 생성
        
        Args:
            question: 질문
            
        Returns:
            Dict: 답변 및 소스 문서
        """
        qa_chain = self.create_qa_chain()
        result = qa_chain.invoke({"query": question})
        
        # 결과 포맷팅
        response = {
            "question": question,
            "answer": result["result"],
            "source_documents": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in result["source_documents"]
            ]
        }
        
        return response
    
    def simple_query(self, question: str) -> str:
        """
        간단한 질문-답변 (소스 문서 없이)
        
        Args:
            question: 질문
            
        Returns:
            str: 답변
        """
        # 관련 문서 검색
        docs = document_retriever.retrieve_documents(question)
        
        # 컨텍스트 생성
        context = document_retriever.format_documents(docs)
        
        # 프롬프트 생성 및 LLM 호출
        prompt_text = self.prompt.format(context=context, question=question)
        answer = self.llm.invoke(prompt_text)
        
        return answer


# 전역 인스턴스
qa_chain_manager = QAChainManager()

