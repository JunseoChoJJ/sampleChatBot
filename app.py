import streamlit as st
import requests
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="채용 공고 챗봇",
    page_icon="💼",
    layout="wide"
)

# 백엔드 URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

# 타이틀
st.title("💼 채용 공고 안내 챗봇")
st.caption(" 데이터 엔지니어 채용에 대해 궁금한 점을 물어보세요!")

# 문서 컨텍스트 사용 설정
use_document = True

# 채팅 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "tokens" in message:
            st.caption(f"토큰: {message['tokens']['total_tokens']} (입력: {message['tokens']['prompt_tokens']}, 출력: {message['tokens']['completion_tokens']})")

# 사용자 입력
if prompt := st.chat_input("궁금한 점을 입력해주세요..."):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 어시스턴트 응답
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # API 호출
            with st.spinner("답변 생성 중..."):
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={
                        "message": prompt,
                        "use_document": use_document
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    assistant_message = data["response"]
                    tokens_used = data["tokens_used"]
                    
                    # 응답 표시
                    message_placeholder.markdown(assistant_message)
                    st.caption(f"모델: {data['model']} | 토큰: {tokens_used['total_tokens']} (입력: {tokens_used['prompt_tokens']}, 출력: {tokens_used['completion_tokens']})")
                    
                    # 메시지 저장
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_message,
                        "tokens": tokens_used
                    })
                    
                    # 토큰 카운트 업데이트
                    st.session_state.total_tokens += tokens_used["total_tokens"]
                    
                else:
                    error_message = f"❌ API 오류: {response.status_code}"
                    message_placeholder.error(error_message)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message
                    })
        
        except requests.exceptions.ConnectionError:
            error_message = "❌ 백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요."
            message_placeholder.error(error_message)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message
            })
        
        except Exception as e:
            error_message = f"❌ 오류 발생: {str(e)}"
            message_placeholder.error(error_message)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message
            })
