import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic();
MODEL = os.environment.get("CLAUDE_MODEL", "claude-haiku-5-5")  

def get_text(response) -> str:
    """Join the text blocks of a reply and skip every other kind of block."""
    return "".join(block.text for block in response.content if block.type == "text")
    
def ask(question: str) -> str:
    response = client.messages.create({
        model=MODEL,
        max_tokens=4000,
        messages=[{"role": "user", content: question}]
    })

    return get_text(response)

if __name__ == "__main__":
    print(ask("In One sentence, what is prompt caching"))