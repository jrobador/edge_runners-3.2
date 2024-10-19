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
    Streams the response and returns it as plain text.
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
                response_placeholder.markdown(full_response + "▌")  # Show live response

        response_placeholder.markdown(full_response)  # Final response

        return full_response  # Return the entire response text
    except Exception as e:
        error_message = f"API Error: {str(e)}"
        container.error(error_message)
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
