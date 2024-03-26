from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms.ollama import Ollama

llm = Ollama(base_url="http://localhost:11434",model="gemma:2b",)

def get_completion_ollama(prompt):
    return llm.invoke(prompt)

prompt = '写一句中文诗词'
res = get_completion_ollama(prompt=prompt)
print(res)