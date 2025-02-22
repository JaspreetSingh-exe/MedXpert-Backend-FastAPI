import re
import json
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load OpenAI API Key securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI Model (GPT-3.5)
llm = ChatOpenAI(name="gpt-3.5-turbo", api_key=OPENAI_API_KEY)

def extract_medical_values(text):
    """
    Extracts numerical medical values from the report using regex.

    Args:
        text (str): Extracted medical report text.

    Returns:
        dict: Extracted medical values as {parameter: value}.
    """
    # Updated regex to capture test names, values, and units correctly
    matches = re.findall(r"([\w\s()%-]+)[\s:-]+([\d.]+)\s*(g/dL|mg/dL|%|x10\^?\d*/?L?)?", text)

    extracted_values = {}
    for match in matches:
        parameter, value, unit = match
        parameter = parameter.strip()
        value = value.strip()
        unit = unit.strip() if unit else ""

        extracted_values[parameter] = f"{value} {unit}".strip()  # Keep units if available

    return extracted_values

def detect_abnormalities_llm(text):
    """
    Uses GPT-3.5 to analyze extracted medical values and detect abnormalities.

    Args:
        text (str): Extracted medical report text.

    Returns:
        dict: JSON response with detected abnormalities.
    """
    extracted_values = extract_medical_values(text)

    if not extracted_values:
        return {"message": "No medical values found for analysis."}

    # Constructing a detailed prompt for LLM
    prompt = f"""
    The following are medical test results extracted from a patient's report:

    {json.dumps(extracted_values, indent=2)}

    Based on your medical knowledge, analyze these values and:
    - Identify any abnormal values.
    - Explain why they might be concerning.
    - Suggest possible medical conditions related to abnormalities.
    - Provide recommendations for further medical consultation.

    Respond in valid JSON format without additional text:
    {{
      "abnormalities": [
        {{
          "parameter": "<Test Name>",
          "value": "<Test Value>",
          "explanation": "<Reason why it's abnormal>",
          "possible_conditions": ["Condition 1", "Condition 2"],
          "recommendations": "Suggested medical advice"
        }}
      ]
    }}
    """

    # Query GPT-3.5 for abnormalities
    try:
        response = llm.invoke(prompt).content  # Use .content to extract response
        parsed_response = json.loads(response)  # Ensure JSON response

        return parsed_response  # Return proper JSON

    except Exception as e:
        return {"error": f"LLM analysis failed: {str(e)}"}
