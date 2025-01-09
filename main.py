from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from Model.script import get_predictions
from pydantic import BaseModel
import json

app = FastAPI()
  
origins = ['http://localhost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# class StockInput(BaseModel):
#     ticker:str
# @app.post("/api/predict")
# async def get_future_stocks(data:StockInput):
#     symbol = data.ticker
#     prices = get_predictions(symbol)
#     return {"result":prices}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            ticker = message.get("ticker")
            data = get_predictions(ticker)

            await websocket.send_text(json.dumps(data))
            
    except WebSocketDisconnect:
        print("Client disconnected")