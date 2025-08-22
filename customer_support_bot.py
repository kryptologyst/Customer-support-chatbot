import os
import requests
import gradio as gr

# FastAPI service endpoint (configurable via environment variable)
API_URL = os.getenv("CHATBOT_API_URL", "http://localhost:8000/chatbot")


def chatbot_response(user_query: str, language: str = "English") -> str:
    """
    Calls the local FastAPI chatbot endpoint and returns the response text.
    """
    if not user_query or not user_query.strip():
        return "Please enter a question."

    try:
        resp = requests.post(
            API_URL,
            json={"query": user_query.strip(), "language": language},
            timeout=30,
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("response", "No answer available.")
        return f"API error: {resp.status_code}"
    except requests.Timeout:
        return "The request timed out. Please try again."
    except Exception:
        return "Unexpected error talking to the API. Ensure it is running."


# Create Gradio interface
interface = gr.Interface(
    fn=chatbot_response,
    inputs=[
        gr.Textbox(lines=2, placeholder="Ask your customer support question...", label="Question"),
        gr.Dropdown(choices=["English", "Spanish", "French", "German"], value="English", label="Language"),
    ],
    outputs=gr.Textbox(label="Chatbot Response"),
    title="AI-Powered Customer Support Chatbot",
    description="Ask a question; the service will respond using the configured model.",
)

# Launch the web app
if __name__ == "__main__":
    interface.launch()





# # Test Customer Support Chatbot
# if __name__ == "__main__":
#     sample_query = "How can I return a product?"
#     print("### Chatbot Response ###")
#     print(chatbot_response(sample_query))







