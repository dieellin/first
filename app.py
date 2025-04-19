from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import uvicorn
from model.agent import Agent
from utils.web_search import search_web

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create an instance of the agent
agent = Agent()

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def get_home():
    with open("frontend/index.html", "r") as f:
        return f.read()


@app.post("/api/chat")
async def chat(request_data: dict):
    try:
        message = request_data.get("message", "")
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")

        response = agent.process_message(message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            message = data.get("message", "")

            # Process the message through the agent with streaming
            async for chunk in agent.process_message_stream(message):
                await websocket.send_text(json.dumps({"chunk": chunk}))

            # Send a completion signal
            await websocket.send_text(json.dumps({"done": True}))
    except Exception as e:
        await websocket.send_text(json.dumps({"error": str(e)}))
        await websocket.close()


@app.post("/api/train")
async def train_model(request_data: dict):
    try:
        data_path = request_data.get("data_path", "data/processed")
        epochs = request_data.get("epochs", 5)

        result = agent.train(data_path, epochs)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search")
async def search(request_data: dict):
    try:
        query = request_data.get("query", "")
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")

        results = search_web(query)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)