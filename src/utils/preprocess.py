import re

def preprocess_text(text: str) -> str:
    """
    process text before passing to model
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9]", " ", text)
    return text

