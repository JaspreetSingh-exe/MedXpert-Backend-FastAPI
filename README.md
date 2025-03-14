# MedXpert Backend (FastAPI)

## 📌 Overview
MedXpert Backend is the core API server for the MedXpert application, built using **FastAPI**. It enables users to upload medical reports in **PDF or image format**, processes them using **OCR and AI models**, and provides a detailed summary along with **abnormality detection**. Additionally, it features a **chatbot** that can answer user queries based on the medical report data. This backend is designed to be **fast, scalable, and secure**, leveraging modern cloud technologies like **Google Cloud Run** for seamless deployment.

This project aims to make medical reports more understandable by extracting key health indicators and explaining them in simpler terms using **AI-powered natural language processing**.

---

## 🏥 Problem Statement & Why MedXpert is Useful
### **The Challenge:**
Understanding medical reports can be challenging for non-medical professionals. Many patients struggle to interpret complex test results, abnormal values, and medical terminology. Additionally, doctors often have limited time to explain reports in detail, leaving patients uncertain about their health conditions.

### **How MedXpert Solves This Problem:**
✅ **Extracts Medical Data:** Automatically extracts text from PDF and image-based reports using **OCR (Tesseract, pdfplumber)**.  
✅ **Summarizes Reports:** Converts complex medical language into **simplified, understandable summaries** using **AI (OpenAI GPT-3.5)**.  
✅ **Detects Abnormalities:** Identifies abnormal values and highlights potential health concerns using **AI-driven analysis**.  
✅ **Provides AI-Powered Chatbot:** Allows users to ask questions about their medical reports and get **instant explanations** using **LLM-based responses**.  
✅ **Improves Accessibility:** Enables easy understanding of health reports, empowering patients to make **informed medical decisions**.  

With MedXpert, users can confidently **analyze their reports, detect potential health risks, and seek appropriate medical consultations faster.**

---

## 🚀 Features
- 📄 **Upload & Process Medical Reports** (PDF, Images)
  ```python
  @app.post("/upload/")
  async def upload_report(file: UploadFile = File(...)):
      report_data = await process_medical_report(file)
      return report_data
  ```
- 📝 **Summarize Medical Reports** into simple, easy-to-understand text
  ```python
  from langchain.chains.summarize import load_summarize_chain
  summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
  summary = summary_chain.run(docs)
  ```
- 🔍 **Detect Medical Abnormalities** using AI
  ```python
  from api.abnormality_checker import detect_abnormalities_llm
  abnormalities = detect_abnormalities_llm(extracted_text)
  ```
- 🤖 **Chatbot for Medical Queries**
  ```python
  @router.post("/chat/")
  async def chat_with_ai(question: str):
      report = get_latest_report()
      response = llm.invoke(question)
      return {"response": response.content}
  ```
- 📑 **Automatic API Documentation (Swagger UI)**
  ```python
  from fastapi.openapi.utils import get_openapi
  @app.get("/openapi.json")
  async def get_open_api_endpoint():
      return get_openapi(title="MedXpert API", version="1.0.0", routes=app.routes)
  ```

---

## 📂 Project Structure
```
MedXpert-Backend-FastAPI/
│── api/                            # API Endpoint
│   │── abnormality_checker.py      # Detects medical abnormalities in reports
│   │── chatbot.py                  # AI Chatbot for medical queries
│   │── report_processor.py         # Handles report processing (PDFs/Images)
│   │── main.py                     # Main API entry point (FastAPI setup)
│
│── utils/                          # Utility functions
│   │── ocr_utils.py                # Extracts text from images using OCR
│   │── pdf_utils.py                # Extracts text from PDFs using pdfplumber
│
│── .gitignore                      # Ignore unnecessary files (e.g., .env)
│── requirements.txt                # Python dependencies
│── README.md                       # Project documentation
│── LICENSE                         # Open-source license
```
---    

## 🔧 Installation & Setup

### 1️⃣ Clone the Repository
First, clone the project repository from GitHub. This will download all necessary files to your local machine.
```bash
git clone https://github.com/JaspreetSingh-exe/MedXpert-Backend-FastAPI.git
cd MedXpert-Backend-FastAPI
```

### 2️⃣ Create and Activate a Virtual Environment
A virtual environment ensures that dependencies do not conflict with system-wide Python packages.
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3️⃣ Install Dependencies
Install all required Python packages specified in `requirements.txt`.
```bash
pip install -r requirements.txt
```
This includes libraries like **FastAPI**, **pdfplumber**, **Tesseract OCR**, and **OpenAI API**.

### 4️⃣ Set Up Environment Variables
Create a `.env` file to store your sensitive credentials and API keys.
```bash
touch .env
```
Then, open the `.env` file and add your API key:
```env
OPENAI_API_KEY=your-api-key
PORT=8080
```

Load the environment variables securely in your Python code:
```python
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

### 5️⃣ Run the Server
Finally, start the FastAPI backend using Uvicorn.
```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```
The `--reload` flag ensures that the server automatically updates when code changes.

---

## 🚀 Deploying with Docker & Google Cloud Run
To deploy the **MedXpert Backend** using **Docker** and **Google Cloud Run**, follow these steps:

### **1️⃣ Create a Dockerfile**
Create a `Dockerfile` in the root directory and add the following content:
```dockerfile
# Use official Python image
FROM python:3.9

# Set working directory inside the container
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI runs on
EXPOSE 8080

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### **2️⃣ Build & Tag the Docker Image**
```bash
docker build -t medxpert-backend .
```

### **3️⃣ Test the Container Locally**
```bash
docker run -p 8080:8080 medxpert-backend
```
Check `http://localhost:8080/docs` to confirm the API is working.

### **4️⃣ Push the Docker Image to Google Container Registry**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

docker tag medxpert-backend gcr.io/YOUR_PROJECT_ID/medxpert-backend

docker push gcr.io/YOUR_PROJECT_ID/medxpert-backend
```

### **5️⃣ Deploy to Google Cloud Run**
```bash
gcloud run deploy medxpert-backend \
  --image=gcr.io/YOUR_PROJECT_ID/medxpert-backend \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated
```
Once deployed, Google Cloud Run will provide a **URL** where your API is accessible.  


---

## 📜 API Documentation
### **1️⃣ Upload Medical Report**
**Endpoint:** `POST /upload/`
- **Description:** Uploads a medical report (PDF/Image) and processes it.
- **Request:** `multipart/form-data`
  ```json
  {
    "file": "report.pdf"
  }
  ```
- **Response:**
  ```json
  {
  "summary": "Yash M. Patel, a 21-year-old male, had his blood tested at Drlogy Pathology Lab in Mumbai and was found to have low hemoglobin levels, indicating possible anemia or blood loss. Further testing is recommended to determine the underlying cause. The report also indicates high levels of red blood cells, suggesting a possible diagnosis of polycythemia vera, a bone marrow disorder. The report was generated by Medical Lab Technicians Dr. Payal Shah and Dr. Vimal Shah on December 2, 202X at 5:00 PM.",
  "abnormalities": {
    "abnormalities": [
      {
        "parameter": "Blood Hemoglobin (Hb)",
        "value": "12.5",
        "explanation": "Low hemoglobin levels can indicate anemia, which may lead to fatigue, weakness, and shortness of breath.",
        "possible_conditions": [
          "Iron deficiency anemia",
          "Vitamin B12 deficiency anemia"
        ],
        "recommendations": "Further evaluation by a healthcare provider for possible supplementation and treatment."
      }
    ]
  }

  ```

### **2️⃣ Chat with AI (Medical Assistant)**
**Endpoint:** `POST /chat/chat/`
- **Description:** Ask questions based on the latest uploaded report.
- **Request:** `application/json`
  ```json
  {
    "question": "Do I need to see a doctor?"
  }
  ```
- **Response:**
  ```json
  {
    "response": "Yes, based on the abnormalities detected in your medical report, it is recommended that you see a healthcare provider for further evaluation and possible treatment. Low hemoglobin levels and high red blood cell counts can indicate underlying health conditions that may require medical attention. It is important to follow up with a doctor to determine the cause of these abnormalities and to receive appropriate care."
  }
  ```

Once the server is running, you can access the API documentation at:
- **Swagger UI:** [http://localhost:8080/docs](http://localhost:8080/docs)
- **ReDoc:** [http://localhost:8080/redoc](http://localhost:8080/redoc)

---

## ⚠️ Error Handling & Response Codes
This API follows **RESTful error handling** principles, ensuring clear and meaningful responses.

| Status Code | Meaning | Possible Cause |
|------------|---------|---------------|
| **200** ✅ | Success | API call successful |
| **400** ❌ | Bad Request | Invalid input or file format |
| **401** ❌ | Unauthorized | Invalid API Key or missing authentication |
| **404** ❌ | Not Found | Resource not found |
| **500** ❌ | Internal Server Error | Server failure, possible bug |

### **Example Error Response:**
```json
{
  "error": "Invalid file format. Only PDF and image files are supported."
}
```

---

## 🚀 Future Work & Enhancements
### **1️⃣ Medical Image Classification (MRI, X-rays, CT Scans)**
- **Integration of Deep Learning Models:** Future iterations will incorporate **CNN (Convolutional Neural Networks)** for classifying medical images like **X-rays, MRIs, and CT scans**.
- **Use of Pre-trained Models:** Models such as **ResNet, VGG16, EfficientNet**, and **Vision Transformers (ViTs)** will be explored to enhance accuracy.
- **Implementation of DICOM Support:** We aim to support **DICOM format** for medical imaging to ensure compatibility with hospital systems.
- **Example using TensorFlow/Keras:**
  ```python
  from tensorflow.keras.applications import ResNet50
  from tensorflow.keras.preprocessing import image
  import numpy as np

  model = ResNet50(weights="imagenet")
  img = image.load_img("xray_image.jpg", target_size=(224, 224))
  img_array = image.img_to_array(img)
  img_array = np.expand_dims(img_array, axis=0)
  predictions = model.predict(img_array)
  print(predictions)
  ```

### **2️⃣ Real-time Health Risk Prediction**
- **Predictive Analytics using AI:** Integration of AI models that can **predict potential health risks** based on medical history and test results.
- **Integration with Wearables:** Future versions may connect with **smartwatches and health monitoring devices** to provide real-time risk assessments.

### **3️⃣ Expansion to Multi-Language Support**
- **Using NLP for Medical Translation:** The chatbot will be enhanced with **multi-language support**, making medical information accessible to a wider audience.
- **Translation APIs like Google Translate or OpenAI Whisper** will be used for automatic language detection and translation.

### **4️⃣ Cloud AI Processing for Scalability**
- **Using Google Cloud AI and AWS SageMaker:** Future enhancements will leverage **cloud-based AI models** to scale medical report analysis for larger datasets.
- **Serverless Processing:** Auto-scaling infrastructure using **Google Cloud Run and AWS Lambda**.

These improvements will help MedXpert evolve into a **comprehensive AI-powered medical assistant** for both patients and healthcare providers. 🚀
 
---   


## 📂 Frontend Integration

The MedXpert Android app acts as the user interface for interacting with the MedXpert Backend API. It handles user inputs, file uploads, and presents the backend-processed data in a clean, user-friendly way.


### 🚀 How the Frontend Uses the Backend:

- **Medical Report Upload**:  
  Users select and upload PDF or image-based medical reports directly through the app. The frontend sends these files to the backend API for processing and awaits the extracted data and analysis.

- **Displaying Summarized Reports**:  
  After processing, the backend returns a simplified summary of the medical report. The frontend displays this summary in an easy-to-read format for users to understand their health status.

- **Abnormality Highlights**:  
  The backend detects abnormal medical values and flags them. The frontend receives this data and visually highlights these abnormalities within the report summary screen to grab the user’s attention.

- **User Role Enforcement**:  
  The backend tracks user activity (uploads and chatbot usage). Based on the backend's response, the frontend manages feature restrictions (like limiting uploads for guest users).

- **Chatbot Integration**:  
  The frontend provides a chatbot interface where users can ask health-related questions. These questions are sent to the backend, and the frontend displays the AI-generated responses to the user in real time.


### 🔗 FrontEnd Repository  
*This repository contains the complete frontend code for the MedXpert Android application along with the APK for direct download.*    
👉 [MedXpert-FrontEnd Repository](https://github.com/JaspreetSingh-exe/MedXpert-FrontEnd)

---  


## 🤝 Open for Contributions
We welcome contributions from developers, AI researchers, and medical professionals to enhance the MedXpert Backend! If you would like to contribute, here’s how you can help:

### **How to Contribute**
1. **Fork the Repository**: Click on the "Fork" button at the top right of this repository.
2. **Clone Your Fork**: Clone the repository to your local machine.
   ```bash
   git clone https://github.com/JaspreetSingh-exe/MedXpert-Backend-FastAPI.git
   cd MedXpert-Backend-FastAPI
   ```
3. **Create a New Branch**: Make sure to create a new branch for your changes.
   ```bash
   git checkout -b feature-new-enhancement
   ```
4. **Make Your Changes**: Add new features, fix bugs, or improve documentation.
5. **Commit and Push**: Commit your changes and push to your fork.
   ```bash
   git add .
   git commit -m "Added a new feature"
   git push origin feature-new-enhancement
   ```
6. **Create a Pull Request**: Submit a pull request (PR) to the `main` branch of this repository.

### **Guidelines for Contributions**
- Follow best practices for **code structure, comments, and documentation**.
- Ensure that your code **passes all tests and does not break existing functionality**.
- If adding a new feature, please **update the documentation accordingly**.
- Be **respectful and collaborative** when reviewing and discussing PRs.

### **Looking for Inspiration?**
Here are some areas where you can contribute:
- Improve **Medical Image Processing** for **MRI/X-ray classification**.
- Optimize the **AI Chatbot** responses for medical inquiries.
- Enhance **OCR accuracy** for extracting structured medical data.
- Add **multi-language support** for wider accessibility.

Join me in making **MedXpert a powerful and intelligent AI-based medical report analyzer**! 🚀

---

## 📞 Support
If you encounter any issues, feel free to create an issue on GitHub.   
For any queries reach out at `jaspreetsingh01110@gmail.com`

---

## 📜 License
This project is licensed under the **Apache License 2.0**. See `LICENSE` for details.     
   
---   

> ⭐ Don't forget to **star** this repo if you like the project!


