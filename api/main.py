import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, UploadFile, File
from api.report_processor import process_medical_report
from api.chatbot import router as chatbot_router

app = FastAPI(title="Medical Report Analyzer API")

# Include chatbot endpoint
app.include_router(chatbot_router, prefix="/chat", tags=["Chatbot"])

@app.post("/upload/")
async def upload_report(file: UploadFile = File(...)):
    """
    API to upload and process medical reports.
    """
    report_data = await process_medical_report(file)
    return report_data

if __name__ == "__main__":
    import uvicorn

    # Use the PORT provided by Google Cloud Run, default to 8080
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
