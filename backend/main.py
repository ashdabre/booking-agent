from fastapi import FastAPI
from pydantic import BaseModel
from backend.agent_graph import run_agent


app = FastAPI()
context_store = {}

class ChatRequest(BaseModel):
    user: str
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    ctx = context_store.get(req.user, {})
    result, new_ctx = run_agent(req.message, ctx)
    context_store[req.user] = new_ctx
    return {"reply": result}
