import requests
import json
from openai import OpenAI
from config.config import Config

def get_api_config(model_name):         # Determining whether the model is hosted remotely or running locally
    """
    Get API base URL and API key based on the model name.
    """
    if model_name.startswith("meta-llama/"):
        return Config.HOSTED_BASE_URL, Config.HOSTED_API_KEY
    elif model_name == "llama3.2":
        return Config.LOCAL_BASE_URL, None    
    else:
        raise ValueError(f"Invalid model name: {model_name}")


def handle_hosted_request(client, model_name, messages, container):
    """
    Handles the hosted Llama model requests via OpenAI's API.
    Streams the response and returns it as a string or structured format.
    """
    try:
        stream = client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=True,
        )
        response_placeholder = container.empty()
        full_response = ""
        
        # Stream the response and handle possible errors
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                response_placeholder.markdown(full_response + "▌")

        response_placeholder.markdown(full_response)

        # Try parsing the full_response into a structured format (e.g., JSON or dict)
        structured_response = parse_full_response(full_response)
        
        return structured_response or full_response
    except Exception as e:
        error_message = f"API Error: {str(e)}"
        container.error(error_message)
        return None

def parse_full_response(response_text):
    """
    Helper function to parse the full_response text into a structured dictionary.
    This would depend on how the Llama model returns its output. 
    In case the response is structured (like in JSON format), we can use json.loads().
    """
    try:
        # Check if the response is in JSON format or some structured text
        # For now, let's assume it's a simple string that needs splitting into sections
        sections = response_text.split("\n\n")
        structured_response = {}

        for section in sections:
            if "Key Legal Points" in section:
                structured_response["key_points"] = section.replace("Key Legal Points:", "").strip()
            elif "Decisions and Judgments" in section:
                structured_response["decisions"] = section.replace("Decisions and Judgments:", "").strip()
            elif "Additional Notes" in section:
                structured_response["notes"] = section.replace("Additional Notes:", "").strip()

        return structured_response
    except Exception as e:
        # If parsing fails, return None (raw string will be used as fallback)
        return None



def handle_local_request(base_url, model_name, messages, container):
    """
    Handles requests to the locally hosted Llama model.
    """
    try:
        payload = {
            "model": model_name,
            "messages": messages,
            "stream": True,
        }
        headers = {"Content-Type": "application/json"}

        response_placeholder = container.empty()
        full_response = ""

        with requests.post(
            base_url, json=payload, headers=headers, stream=True
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if "done" in chunk and chunk["done"]:
                            break
                        if "message" in chunk and "content" in chunk["message"]:
                            content = chunk["message"]["content"]
                            full_response += content
                            response_placeholder.markdown(full_response + "▌")
                    except json.JSONDecodeError:
                        pass
        response_placeholder.markdown(full_response)
        return full_response
    except requests.RequestException as e:
        error_message = f"API Error: {str(e)}"
        container.error(error_message)
        return None


def stream_response(messages, container, model_name):
    """
    This function handles the API request based on the model (hosted or local) and streams the response.
    """
    base_url, api_key = get_api_config(model_name)

    if model_name.startswith("meta-llama/"):
        client = OpenAI(api_key=api_key, base_url=base_url)
        return handle_hosted_request(client, model_name, messages, container)
    elif model_name == "llama3.2":
        return handle_local_request(base_url, model_name, messages, container)
    else:
        raise ValueError("Unsupported model selected.")
