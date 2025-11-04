"""
Streamlit UI - LangChain RAG 시스템 테스트 인터페이스
"""
import streamlit as st
import requests
import json

# 페이지 설정
st.set_page_config(
    page_title="LangChain RAG 시스템",
    page_icon="🤖",
    layout="wide"
)

# API 엔드포인트
API_BASE_URL = "http://localhost:8000"

# 제목
st.title("🤖 LangChain RAG 시스템")
st.markdown("---")

# 사이드바 - 설정
with st.sidebar:
    st.header("⚙️ 설정")
    
    # API 서버 상태 확인
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            st.success("✅ API 서버 연결됨")
        else:
            st.error("❌ API 서버 오류")
    except:
        st.error("❌ API 서버 연결 실패")
        st.info("서버를 실행해주세요:\n```bash\npython main.py\n```")
    
    st.markdown("---")
    
    # 온도 설정
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    
    # Top-K 설정
    top_k = st.slider("검색 문서 개수 (Top-K)", 1, 10, 4, 1)
    
    st.markdown("---")
    st.markdown("### 📊 문서 정보")
    
    # 문서 정보 조회
    if st.button("🔄 문서 정보 새로고침"):
        try:
            response = requests.get(f"{API_BASE_URL}/api/rag/documents")
            if response.status_code == 200:
                doc_info = response.json()
                st.metric("총 문서 청크", doc_info.get("total_chunks", 0))
                st.metric("업로드된 파일", len(doc_info.get("uploaded_files", [])))
        except Exception as e:
            st.error(f"오류: {str(e)}")

# 탭 생성
tab1, tab2, tab3 = st.tabs(["💬 일반 채팅", "📄 RAG 질의응답", "📤 문서 업로드"])

# 탭 1: 일반 채팅
with tab1:
    st.header("💬 일반 채팅")
    st.markdown("Ollama LLM과 직접 대화합니다.")
    
    # 채팅 히스토리 초기화
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # 채팅 히스토리 표시 (먼저 표시)
    for chat in st.session_state.chat_history:
        with st.container():
            st.markdown(f"**👤 사용자:**")
            st.info(chat["user"])
            st.markdown(f"**🤖 AI:**")
            st.success(chat["assistant"])
            st.markdown("---")
    
    # 채팅 입력 (엔터로 전송)
    chat_input = st.chat_input("메시지를 입력하세요 (Enter로 전송)")
    
    # 대화 기록 지우기 버튼
    if st.button("🗑️ 대화 기록 지우기", key="chat_clear"):
        st.session_state.chat_history = []
        st.rerun()
    
    # 메시지 전송 처리
    if chat_input:
        with st.spinner("응답 생성 중..."):
            try:
                # 대화 히스토리를 API 형식으로 변환
                history = []
                for chat in st.session_state.chat_history:
                    history.append({"role": "user", "content": chat["user"]})
                    history.append({"role": "assistant", "content": chat["assistant"]})
                
                response = requests.post(
                    f"{API_BASE_URL}/api/chat/query",
                    json={
                        "message": chat_input,
                        "temperature": temperature,
                        "history": history
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.chat_history.append({
                        "user": chat_input,
                        "assistant": result["response"]
                    })
                    st.rerun()  # 화면 새로고침
                else:
                    st.error(f"오류: {response.status_code}")
            except Exception as e:
                st.error(f"오류: {str(e)}")

# 탭 2: RAG 질의응답
with tab2:
    st.header("📄 RAG 질의응답")
    st.markdown("업로드된 문서를 기반으로 답변합니다.")
    
    # RAG 히스토리 초기화
    if "rag_history" not in st.session_state:
        st.session_state.rag_history = []
    
    # 질문 입력
    rag_input = st.text_area("질문을 입력하세요:", height=100, key="rag_input")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("🔍 검색 및 답변", key="rag_search"):
            if rag_input:
                with st.spinner("문서 검색 및 답변 생성 중..."):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/api/rag/query",
                            json={
                                "question": rag_input,
                                "top_k": top_k
                            }
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.session_state.rag_history.append(result)
                        else:
                            error_detail = response.json().get("detail", "알 수 없는 오류")
                            st.error(f"오류: {error_detail}")
                    except Exception as e:
                        st.error(f"오류: {str(e)}")
    
    with col2:
        if st.button("🗑️ 질의 기록 지우기", key="rag_clear"):
            st.session_state.rag_history = []
            st.rerun()
    
    # RAG 히스토리 표시
    st.markdown("---")
    for idx, item in enumerate(reversed(st.session_state.rag_history)):
        with st.expander(f"🔍 질문 {len(st.session_state.rag_history) - idx}: {item['question']}", expanded=(idx == 0)):
            st.markdown("**🤖 답변:**")
            st.success(item["answer"])
            
            st.markdown("**📚 참고 문서:**")
            for i, doc in enumerate(item["source_documents"], 1):
                with st.container():
                    st.markdown(f"*문서 {i}*")
                    st.text_area(
                        f"내용 {i}:",
                        doc["content"],
                        height=100,
                        key=f"doc_{idx}_{i}",
                        disabled=True
                    )
                    if doc.get("metadata"):
                        st.json(doc["metadata"])

# 탭 3: 문서 업로드
with tab3:
    st.header("📤 문서 업로드")
    st.markdown("PDF, TXT, MD 파일을 업로드하여 벡터 DB에 저장합니다.")
    
    # 파일 업로더
    uploaded_file = st.file_uploader(
        "파일을 선택하세요",
        type=["pdf", "txt", "md"],
        help="PDF, TXT, Markdown 파일을 업로드할 수 있습니다."
    )
    
    if uploaded_file is not None:
        st.info(f"선택된 파일: {uploaded_file.name} ({uploaded_file.size} bytes)")
        
        if st.button("📤 업로드 및 벡터화"):
            with st.spinner("파일 업로드 및 처리 중..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    response = requests.post(
                        f"{API_BASE_URL}/api/rag/upload",
                        files=files
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ 업로드 성공!")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("파일명", result.get("filename", "N/A"))
                        with col2:
                            st.metric("생성된 청크", result.get("chunks", 0))
                        with col3:
                            st.metric("전체 문서", result.get("total_documents", 0))
                    else:
                        error_detail = response.json().get("detail", "알 수 없는 오류")
                        st.error(f"업로드 실패: {error_detail}")
                except Exception as e:
                    st.error(f"오류: {str(e)}")
    
    st.markdown("---")
    
    # 문서 관리
    st.subheader("📊 저장된 문서 관리")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 문서 목록 조회"):
            try:
                response = requests.get(f"{API_BASE_URL}/api/rag/documents")
                if response.status_code == 200:
                    doc_info = response.json()
                    
                    st.metric("총 문서 청크", doc_info.get("total_chunks", 0))
                    
                    uploaded_files = doc_info.get("uploaded_files", [])
                    if uploaded_files:
                        st.markdown("**업로드된 파일:**")
                        for file in uploaded_files:
                            st.write(f"- {file['filename']} ({file['size']} bytes)")
                    else:
                        st.info("업로드된 파일이 없습니다.")
            except Exception as e:
                st.error(f"오류: {str(e)}")
    
    with col2:
        if st.button("🗑️ 모든 문서 삭제", type="secondary"):
            if st.checkbox("정말로 삭제하시겠습니까?"):
                try:
                    response = requests.delete(f"{API_BASE_URL}/api/rag/documents")
                    if response.status_code == 200:
                        st.success("✅ 모든 문서가 삭제되었습니다.")
                    else:
                        st.error("삭제 실패")
                except Exception as e:
                    st.error(f"오류: {str(e)}")

# 푸터
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>🤖 LangChain + Ollama RAG 시스템</p>
        <p><small>FastAPI 서버가 http://localhost:8000 에서 실행 중이어야 합니다.</small></p>
    </div>
    """,
    unsafe_allow_html=True
)

