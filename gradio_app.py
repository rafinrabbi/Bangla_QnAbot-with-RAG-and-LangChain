# gradio_client.py
import gradio as gr
import requests

API_URL = "http://localhost:8000/ask"  

def ask_question_to_api(message, history):
    try:
        response = requests.post(API_URL, json={"question": message})
        if response.status_code == 200:
            return response.json().get("answer", "No answer found.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Exception: {e}"

gr.ChatInterface(
    ask_question_to_api,
    textbox=gr.Textbox(
        placeholder="Ask your question...",
        container=False,
        autoscroll=True,
        scale=7
    ),
    title="বাংলা প্রথম পত্র 'অপরিচিতা' বিষয়ক আলোচনা এবং প্রশ্ন-উত্তর"
).launch()


