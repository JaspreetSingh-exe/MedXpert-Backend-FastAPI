import sys
import os

# Add script directory and project root to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
from api.abnormality_checker import detect_abnormalities_llm
from utils.pdf_utils import extract_text_from_pdf
from utils.ocr_utils import extract_text_from_image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize GPT-3.5 model
llm = ChatOpenAI(name="gpt-3.5-turbo", api_key=OPENAI_API_KEY)

# Temporary storage for the latest report (No database)
latest_report = None


def extract_text(file, file_extension):
    """
    Extracts text from the uploaded file based on its type (PDF or Image).
    """
    if file_extension == "pdf":
        return extract_text_from_pdf(file)
    elif file_extension in ["png", "jpg", "jpeg"]:
        return extract_text_from_image(file)
    else:
        return None


async def process_medical_report(file):
    """
    Processes the uploaded medical report (PDF or Image),
    extracts text, summarizes the content using OpenAI GPT,
    and detects medical abnormalities.
    """
    global latest_report  # Store the latest uploaded report

    # Read file bytes
    contents = await file.read()

    # Determine file type and extract text
    file_extension = file.filename.split(".")[-1].lower()
    extracted_text = extract_text(contents, file_extension)

    if not extracted_text:
        return {"error": "Unsupported file format or no text found."}

    # Split text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    text_chunks = text_splitter.split_text(extracted_text)

    # Convert text into LangChain Document format
    docs = [Document(page_content=chunk) for chunk in text_chunks]

    # Summarization using GPT-3.5
    try:
        summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = summary_chain.run(docs)
    except Exception as e:
        return {"error": f"Summarization failed: {str(e)}"}

    # Detect abnormalities using LLM
    abnormalities = detect_abnormalities_llm(extracted_text)

    # Store latest report in memory
    latest_report = {
        "summary": summary,
        "abnormalities": abnormalities
    }

    return {"summary": summary, "abnormalities": abnormalities}


def get_latest_report():
    """
    Returns the latest uploaded medical report stored in memory.
    """
    return latest_report