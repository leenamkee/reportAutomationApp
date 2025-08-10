import streamlit as st
from utils.file_loader import load_files
from utils.prompt import generate_report_prompt, followup_question_prompt
from agent.report_agent import create_report_agent

st.set_page_config(page_title="업무보고서 생성기", layout="wide")
st.title("📄 업무보고서 자동 생성 앱")

uploaded_files = st.file_uploader(
    "문서를 업로드하세요 (PDF, TXT, 최대 5개)",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

user_guide = st.text_area("보고서 작성 가이드를 입력하세요", placeholder="예: 마케팅 성과 강조, 수치 중심으로 정리 등")

if st.button("보고서 생성") and uploaded_files:
    with st.spinner("문서 분석 및 보고서 작성 중..."):
        documents = load_files(uploaded_files)
        context = "\n\n".join(documents)
        full_prompt = generate_report_prompt(context, user_guide)
        report_agent = create_report_agent()
        response = report_agent.invoke({"input": full_prompt})
        # st.session_state["report"] = initial_report["output"]
        st.session_state["report"] = response.content  # 여기만 이렇게 수정
        st.session_state["agent"] = report_agent
        st.success("보고서가 생성되었습니다!")

if "report" in st.session_state:
    st.subheader("📝 생성된 업무보고서")
    st.text_area("초안", value=st.session_state["report"], height=400)

    followup_prompt = followup_question_prompt(st.session_state['report'])

    # followup_prompt = f"""
    # 다음 보고서를 기반으로, 
    # 1. 사용자가 AI에게 추가로 요청할 수 있는 질문 예시 2~3가지
    # 2. 이 보고서의 완성도를 높이기 위해 필요한 정보나 자료 2~3가지

    # 를 각각 제안해 주세요.

    # 보고서:
    # {st.session_state['report']}
    # """

    result = st.session_state["agent"].invoke({"input": followup_prompt})
    st.session_state["ai_suggestions"] = result.content
    if "ai_suggestions" in st.session_state:
        with st.expander("💡 AI가 제안한 질문 및 자료 추천", expanded=True):
            st.markdown(st.session_state["ai_suggestions"])

    user_edit = st.chat_input("보고서에 대해 추가 요청해 보세요 (예: 더 요약해줘)")
    if user_edit:
        follow_up = f"{st.session_state['report']}\n\n사용자 추가 요청: {user_edit}"
        followup_prompt = generate_report_prompt(follow_up, user_guide)
        with st.spinner("요청 반영 중..."):
            updated = st.session_state["agent"].invoke({"input": followup_prompt})
            st.session_state["report"] = updated.content
            st.rerun()
