from openai import OpenAI
import streamlit as st
import time

def load_css():
    # 모던하고 미래적인 스타일을 위한 CSS
    css = """
    <style>
        body, .stApp, .stChatFloatingInputContainer {
            background-color: #0E0E0E !important; /* 다크 모드 배경색 */
            color: #FFFFFF; /* 텍스트 색상 */
            font-family: 'Roboto', sans-serif; /* 폰트 설정 */
        }
        .stChatInputContainer {
            background-color: #1E1E1E !important; /* 입력 필드 배경색 */
            border-radius: 10px; /* 둥근 모서리 */
        }
        textarea {
            background-color: #2E2E2E !important; /* 실제 입력 필드 배경색 */
            color: #FFFFFF !important; /* 텍스트 색상 */
            border: none; /* 테두리 제거 */
            border-radius: 5px; /* 둥근 모서리 */
            padding: 10px; /* 내부 여백 */
        }
        .stButton>button {
            background-color: #6200EE !important; /* 버튼 배경색 */
            color: #FFFFFF !important; /* 버튼 텍스트 색상 */
            border: none; /* 버튼 테두리 제거 */
            border-radius: 5px; /* 둥근 모서리 */
            padding: 10px 20px; /* 버튼 패딩 */
            font-size: 16px; /* 버튼 텍스트 크기 */
            transition: background-color 0.3s ease; /* 배경색 변경 애니메이션 */
        }
        .stButton>button:hover {
            background-color: #3700B3 !important; /* 버튼 호버 시 배경색 */
        }
        .stMarkdown {
            color: #BB86FC; /* 링크 텍스트 색상 */
        }
        .stDivider {
            background-color: #BB86FC !important; /* 구분선 색상 */
        }
        .stSidebar {
            background-color: #121212 !important; /* 사이드바 배경색 */
            border-right: 1px solid #BB86FC; /* 사이드바 오른쪽 테두리 */
        }
        .stSidebar .stButton>button {
            background-color: #03DAC5 !important; /* 사이드바 버튼 배경색 */
            color: #000000 !important; /* 사이드바 버튼 텍스트 색상 */
        }
        .stSidebar .stButton>button:hover {
            background-color: #018786 !important; /* 사이드바 버튼 호버 시 배경색 */
        }
        .stChatMessage {
            background-color: #1E1E1E !important; /* 채팅 메시지 배경색 */
            border-radius: 10px; /* 둥근 모서리 */
            padding: 10px; /* 내부 여백 */
            margin-bottom: 10px; /* 아래 여백 */
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); /* 그림자 효과 */
        }
        .stChatMessage.assistant {
            border-left: 5px solid #03DAC5; /* assistant 메시지 왼쪽 테두리 */
        }
        .stChatMessage.user {
            border-left: 5px solid #BB86FC; /* user 메시지 왼쪽 테두리 */
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .stChatMessage {
            animation: fadeIn 0.5s ease;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def start_thread(client):
    try:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id  # 스레드 ID를 session_state에 저장
        st.success("대화가 시작되었습니다!")
    except Exception as e:
        st.error("대화 시작에 실패했습니다. 다시 시도해주세요.")
        st.error(str(e))

def main():
    load_css()  # 배경색 스타일 로드

    # 초기화 조건 수정
    if "initialized" not in st.session_state:
        st.session_state.thread_id = ""  # 스레드 ID 초기화
        st.session_state.messages = [{"role": "assistant", "content": "안녕하세요, 저는 경상남도 교육청 업무안내 챗봇입니다. 무엇을 도와드릴까요?"}]  # 초기 메시지 설정
        st.session_state.initialized = True

    # API 키 리스트
    api_keys = [
        st.secrets["api_key1"], st.secrets["api_key2"], st.secrets["api_key3"],
        st.secrets["api_key4"], st.secrets["api_key5"], st.secrets["api_key6"]
    ]

    # 업데이트된 Assistant ID
    assistant_id = st.secrets["assistant_api_key1"]
    client = None

    # API 키를 순차적으로 시도하며 OpenAI 객체 생성
    for index, api_key in enumerate(api_keys):
        try:
            client = OpenAI(api_key=api_key)
            break
        except Exception as e:
            st.error(f"API 키 {index + 7} 실패: {str(e)}")
            continue

    if not client:
        st.error("모든 API 키가 실패했습니다.")
        st.stop()

    # 세션 시작 시 자동으로 대화 시작
    if not st.session_state.thread_id:
        start_thread(client)

    with st.sidebar:
        # 스레드 ID 관리
        st.divider()
        if "show_examples" not in st.session_state:
            st.session_state.show_examples = True

        if st.session_state.show_examples:
            st.subheader("질문 예시")
            st.info("메타버스와 관련된 부서는 어디인가요?")
            st.info("수능과 관련된 부서는 어디지 모두 말해주세요.")
            st.info("초등학교 운동장 개방과 관련된 부서는 어디인가요?")

        # Google Drive 파일 다운로드 링크 추가
        st.markdown("[1. 2024년도 결산 주요사업조서(2023년도 예산안-세출만 추출) 다운로드](https://drive.google.com/file/d/1TyKueueI2ZBGVqNkJCLq1RKIeUAXgFz8/view?usp=drive_link)")
        st.markdown("5. 제18대 경상남도교육감 자립공존의 경남혁신교육3기 백서 다운로드](https://drive.google.com/file/d/1zsKSPxAeF8KNTE9o3oNZ6qVHxHeCgAdn/view?usp=drive_link)")

    # 스레드 ID 입력란을 자동으로 업데이트
    thread_id = st.session_state.thread_id

    st.title("경상남도 교육청 업무안내 챗봇")
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if not thread_id:
            st.error("대화 시작에 문제가 발생했습니다. 다시 시도해주세요.")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        response = client.beta.threads.messages.create(
            thread_id,
            role="user",
            content=prompt,
        )

        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        run_id = run.id

        while True:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )
            if run.status == "completed":
                break
            else:
                time.sleep(2)

        thread_messages = client.beta.threads.messages.list(thread_id)

        msg = thread_messages.data[0].content[0].text.value

        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

if __name__ == "__main__":
    main()
