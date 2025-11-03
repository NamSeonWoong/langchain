# LangChain RAG API with Ollama

Ollama와 LangChain을 활용한 **RAG (Retrieval-Augmented Generation)** 시스템입니다.

## 📋 목차

- [기능](#기능)
- [요구사항](#요구사항)
- [설치 방법](#설치-방법)
- [사용 방법](#사용-방법)
- [API 엔드포인트](#api-엔드포인트)
- [설정](#설정)

## ✨ 기능

### 1. 일반 채팅 API
- Ollama LLM과 직접 대화
- 온도(temperature) 조정 가능

### 2. RAG 시스템
- **문서 업로드**: PDF, TXT, Markdown 파일 지원
- **자동 벡터화**: ChromaDB를 사용한 로컬 벡터 저장소
- **문서 기반 질의응답**: 업로드된 문서를 기반으로 정확한 답변 생성
- **소스 추적**: 답변의 근거가 된 문서 조각 제공

## 🔧 요구사항

### 필수 소프트웨어
- **Python**: 3.9 이상
- **Ollama**: 로컬 LLM 서버

### Python 패키지
- FastAPI
- LangChain
- ChromaDB
- 기타 (requirements.txt 참조)

## 📦 설치 방법

### 1. Ollama 설치 및 실행

```bash
# Ollama 설치 (macOS)
brew install ollama

# Ollama 서버 실행
ollama serve

# 모델 다운로드 (새 터미널)
ollama pull llama3.1
ollama pull nomic-embed-text
```

**사용 가능한 모델**:
- LLM: `llama3.1`, `llama3.2`, `mistral`, `gemma2`, `qwen2.5`
- 임베딩: `nomic-embed-text`, `mxbai-embed-large`

### 2. 가상환경 생성 및 활성화

```bash
# 프로젝트 디렉토리로 이동
cd /Users/seonwoong/PycharmProjects/study/llm/langchain

# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 가상환경 활성화 (Windows)
# venv\Scripts\activate
```

### 3. 패키지 설치

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🚀 사용 방법

### 1. 서버 실행

```bash
# 개발 모드 (자동 리로드)
python main.py

# 또는
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. API 문서 확인

브라우저에서 다음 주소로 접속:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. 헬스 체크

```bash
curl http://localhost:8000/health
```

## 🌐 API 엔드포인트

### 기본 엔드포인트

#### `GET /`
- 루트 엔드포인트
- 사용 가능한 API 목록 반환

#### `GET /health`
- 헬스 체크
- Ollama 연결 상태 확인

---

### 채팅 API (`/api/chat`)

#### `POST /api/chat/query`
일반 채팅 질의

**요청 예시**:
```bash
curl -X POST "http://localhost:8000/api/chat/query" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "안녕하세요! 파이썬에 대해 설명해주세요.",
    "temperature": 0.7
  }'
```

**응답 예시**:
```json
{
  "response": "안녕하세요! 파이썬은..."
}
```

#### `GET /api/chat/test`
LLM 연결 테스트

---

### RAG API (`/api/rag`)

#### `POST /api/rag/upload`
문서 업로드 및 벡터화

**요청 예시**:
```bash
curl -X POST "http://localhost:8000/api/rag/upload" \
  -F "file=@document.pdf"
```

**응답 예시**:
```json
{
  "status": "success",
  "message": "문서가 성공적으로 업로드되고 벡터화되었습니다.",
  "filename": "document.pdf",
  "chunks": 25,
  "total_documents": 25
}
```

#### `POST /api/rag/query`
RAG 기반 질의응답

**요청 예시**:
```bash
curl -X POST "http://localhost:8000/api/rag/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "문서의 주요 내용은 무엇인가요?",
    "top_k": 4
  }'
```

**응답 예시**:
```json
{
  "question": "문서의 주요 내용은 무엇인가요?",
  "answer": "문서의 주요 내용은...",
  "source_documents": [
    {
      "content": "관련 문서 내용...",
      "metadata": {"page": 1, "source": "document.pdf"}
    }
  ]
}
```

#### `GET /api/rag/documents`
저장된 문서 정보 조회

**응답 예시**:
```json
{
  "total_chunks": 25,
  "uploaded_files": [
    {
      "filename": "document.pdf",
      "size": 1024000
    }
  ],
  "collection_name": "documents"
}
```

#### `DELETE /api/rag/documents`
모든 문서 삭제

## ⚙️ 설정

`config.py` 파일에서 설정을 변경할 수 있습니다:

```python
# Ollama 설정
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.1"
OLLAMA_EMBEDDING_MODEL = "nomic-embed-text"

# RAG 설정
CHUNK_SIZE = 1000          # 문서 청크 크기
CHUNK_OVERLAP = 200        # 청크 오버랩
TOP_K = 4                  # 검색할 문서 개수

# LLM 파라미터
TEMPERATURE = 0.7
MAX_TOKENS = 2000
```

환경변수로도 설정 가능 (`.env` 파일 생성):
```bash
OLLAMA_MODEL=mistral
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
CHUNK_SIZE=1500
```

## 📁 프로젝트 구조

```
llm/langchain/
├── main.py                 # FastAPI 애플리케이션
├── config.py              # 설정 파일
├── requirements.txt       # 패키지 의존성
├── .gitignore            # Git 제외 파일
├── models/
│   └── llm_setup.py      # LLM 모델 설정
├── rag/
│   ├── document_loader.py # 문서 로더
│   ├── vector_store.py    # 벡터 스토어 관리
│   └── retriever.py       # 문서 검색
├── chains/
│   └── qa_chain.py        # QA 체인
├── routers/
│   ├── chat.py            # 채팅 API
│   └── rag.py             # RAG API
├── data/                  # 업로드 문서 저장
├── chroma_db/            # 벡터 DB (자동 생성)
└── venv/                 # 가상환경 (자동 생성)
```

## 🔍 문제 해결

### Ollama 연결 실패
```bash
# Ollama가 실행 중인지 확인
ps aux | grep ollama

# Ollama 재시작
killall ollama
ollama serve
```

### 모델을 찾을 수 없음
```bash
# 모델 목록 확인
ollama list

# 모델 다운로드
ollama pull llama3.1
ollama pull nomic-embed-text
```

### 포트 충돌
```bash
# 8000번 포트를 사용 중인 프로세스 확인
lsof -i :8000

# 다른 포트로 실행
uvicorn main:app --port 8001
```

## 📝 예제 사용 시나리오

### 1. 문서 업로드 및 질문
```bash
# 1. 문서 업로드
curl -X POST "http://localhost:8000/api/rag/upload" \
  -F "file=@research_paper.pdf"

# 2. 문서 기반 질문
curl -X POST "http://localhost:8000/api/rag/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "이 논문의 핵심 기여는 무엇인가요?"}'
```

### 2. Python을 사용한 API 호출
```python
import requests

# 채팅 API
response = requests.post(
    "http://localhost:8000/api/chat/query",
    json={"message": "파이썬이란?"}
)
print(response.json())

# RAG API
with open("document.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:8000/api/rag/upload",
        files=files
    )
print(response.json())
```

## 🤝 기여

버그 리포트나 기능 제안은 이슈로 등록해주세요!

## 📄 라이선스

MIT License

---

**만든이**: Seonwoong  
**날짜**: 2025-11-03

