import aiohttp
from config import VENICE_API_KEY

USER_MEMORY = {}

def wants_memory(text: str):
    triggers = ["what did i say", "recall", "last message", "before"]
    return any(t in text.lower() for t in triggers)

async def ask_venice(user_id: int, prompt: str):
    memory = USER_MEMORY.get(user_id, [])
    memory.append({"role": "user", "content": prompt})
    memory = memory[-10:]
    USER_MEMORY[user_id] = memory

    payload = {"model": "venice-1","messages": memory}
    headers = {"Authorization": f"Bearer {VENICE_API_KEY}","Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.venice.ai/v1/chat/completions", json=payload, headers=headers) as r:
            data = await r.json()
            answer = data["choices"][0]["message"]["content"]
            memory.append({"role": "assistant", "content": answer})
            USER_MEMORY[user_id] = memory[-10:]
            return answer
