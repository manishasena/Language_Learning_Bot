"""
Language Chat Bot
https://www.youtube.com/watch?v=EiInDFhPRvw
"""

from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
You are a bot to help a user learn Japanese. Make your converations simple to understand for a very beginner. Make your responses only in hiragana and katakana. Do not use kanji. Keep your responses up to 2 sentences.

Here is the conversation history {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model = "gemma3:1b")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def handle_conversation():
    context = ""
    print("welcome to the AI Chatbot. Type 'exit' to quit.")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break

        result = chain.invoke({"context": context, "question": user_input})
        print("Bot: ", result)
        context += f"\nUser: {user_input}\n AI: {result}"

if __name__ == "__main__":
    handle_conversation()