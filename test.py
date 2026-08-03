from config import llm

response = llm.invoke(
    "Reply with only: FinAssist AI is ready."
)

print(response.content)