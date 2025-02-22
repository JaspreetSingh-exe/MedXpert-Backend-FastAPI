from fastapi import APIRouter
from langchain_openai import ChatOpenAI
from api.report_processor import get_latest_report
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

router = APIRouter()

# Load OpenAI API Key securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize GPT-3.5 chatbot
llm = ChatOpenAI(name="gpt-3.5-turbo", api_key=OPENAI_API_KEY)

@router.post("/chat/")
async def chat_with_ai(question: str):
    """
    Simple chatbot that answers user questions based on the latest medical report.
    """
    # Get latest uploaded report
    report = get_latest_report()

    if not report:
        return {"error": "No medical report found. Please upload one first."}

    # Build chatbot prompt
    context = f"""
    User's latest medical report summary:
    {report["summary"]}

    Detected abnormalities:
    {report["abnormalities"]}

    User's question: {question}
    """

    # Get response from GPT-3.5
    response = llm.invoke(context)

    return {"response": response.content}
