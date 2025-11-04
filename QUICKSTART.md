# 🚀 빠른 시작 가이드

## ⚡️ 한 번에 실행하기

### 1단계: Ollama 서버 실행 (별도 터미널)

```bash
ollama serve
```

### 2단계: 프로젝트 실행

```bash
cd /Users/seonwoong/PycharmProjects/study/llm/langchain

# 실행 스크립트에 권한 부여
chmod +x run.sh

# 실행
./run.sh
```

---

## 📋 수동 실행 (단계별)

Ollama가 이미 실행 중이라고 가정합니다.

### 터미널 1: FastAPI 서버

```bash
cd /Users/seonwoong/PycharmProjects/study/llm/langchain
source venv/bin/activate
python main.py
```

서버가 실행되면: http://localhost:8000/docs

### 터미널 2: Streamlit UI

```bash
cd /Users/seonwoong/PycharmProjects/study/llm/langchain
source venv/bin/activate

# Streamlit 설치 (아직 안 했다면)
pip install streamlit

# UI 실행
streamlit run ui_app.py
```

브라우저가 자동으로 열리며: http://localhost:8501

---

## ✅ 실행 전 체크리스트

### 1. Ollama 모델 다운로드 확인

```bash
ollama list
```

**필요한 모델:**
- LLM: `llama3.1` (또는 다른 모델)
- 임베딩: `nomic-embed-text`

**없다면 다운로드:**
```bash
ollama pull llama3.1
ollama pull nomic-embed-text
```

### 2. Ollama 서버 실행 확인

```bash
curl http://localhost:11434/api/tags
```

### 3. 가상환경 및 패키지 확인

```bash
source venv/bin/activate
python -c "import streamlit; print('✅ Streamlit OK')"
```

---

## 🔧 문제 해결

### "Connection refused" 오류

**원인:** Ollama 서버가 실행되지 않음

**해결:**
```bash
ollama serve
```

### "Module not found: streamlit" 오류

**원인:** Streamlit 미설치

**해결:**
```bash
source venv/bin/activate
pip install streamlit
```

### 포트 충돌 (8000 또는 8501)

**원인:** 포트가 이미 사용 중

**해결:**
```bash
# 사용 중인 프로세스 확인
lsof -i :8000
lsof -i :8501

# 프로세스 종료
kill -9 <PID>
```

### "업로드된 문서가 없습니다" 오류

**원인:** RAG 질의응답 시 문서가 없음

**해결:** 먼저 "📤 문서 업로드" 탭에서 PDF/TXT 파일을 업로드하세요.

---

## 🎯 첫 테스트 시나리오

### 1. 일반 채팅 테스트
- **탭**: 💬 일반 채팅
- **입력**: "안녕하세요! 파이썬에 대해 설명해주세요."
- **확인**: AI가 응답하는지 확인

### 2. RAG 시스템 테스트
- **탭**: 📤 문서 업로드
- **동작**: PDF 또는 TXT 파일 업로드
- **탭**: 📄 RAG 질의응답
- **입력**: "문서의 핵심 내용은 무엇인가요?"
- **확인**: 문서 기반 답변과 참고 문서 표시

---

## 📞 도움이 필요하신가요?

1. API 문서 확인: http://localhost:8000/docs
2. README.md 참조
3. config.py에서 설정 변경 가능

