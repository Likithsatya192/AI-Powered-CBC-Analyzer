import os
from langchain_groq import ChatGroq

def get_llm():
    """
    Returns a configured ChatGroq instance.
    Defaults to 'llama-3.3-70b-versatile' or similar high-performing model on Groq.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        # Fallback for dev/demo if key is missing, though this will likely fail execution if called.
        # We'll allow it to return None or raise handling upstream, 
        # but for now let's assume the user will provide it.
        pass
    
    return ChatGroq(
        # User requested "llama-3.3-70b-versatile", mapping to strongest available OSS model on Groq: Llama 3.3 70B
        model="llama-3.3-70b-versatile",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    )
