import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
api_key = st.secrets['OPENAI_API_KEY']

def create_report_agent():
    # 최신 Runnable 방식
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        openai_api_key=api_key
    )

    prompt = PromptTemplate.from_template("{input}")

    chain = prompt | llm  # RunnableSequence 형태로 연결

    return chain