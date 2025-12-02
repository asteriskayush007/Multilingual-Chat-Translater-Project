# backend/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import time
from deep_translator import GoogleTranslator

app = FastAPI(title="LinguaLive Translation WS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections = []
        self.users = {}

    async def connect(self, websocket: WebSocket, username: str):
        # 🔥 Remove old duplicate connections of SAME USER
        for conn in list(self.active_connections):
            if self.users.get(conn) == username:
                try:
                    await conn.close()
                except:
                    pass
                self.active_connections.remove(conn)
                self.users.pop(conn, None)

        # NEW CLEAN CONNECTION
        await websocket.accept()
        self.active_connections.append(websocket)
        self.users[websocket] = username

    def __init__(self):
        self.active_connections = []      
        self.users = {}                  
        self.user_lang = {}              

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.users[websocket] = username

        if username not in self.user_lang:
            self.user_lang[username] = "en"

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        self.users.pop(websocket, None)

    async def broadcast_per_receiver(self, sender_username: str, original_text: str, do_translate: bool = True):
        for conn in list(self.active_connections):
            try:
                receiver = self.users.get(conn)
                target_lang = self.user_lang.get(receiver, "en")

                # Start measuring latency
                start = time.time()

                # Translation
                if do_translate:
                    try:
                        translated_text = GoogleTranslator(
                            source="auto", 
                            target=target_lang
                        ).translate(original_text)
                    except Exception:
                        translated_text = original_text
                else:
                    translated_text = original_text

                # End latency measurement
                latency = (time.time() - start) * 1000  # ms

                payload = {
                    "sender": sender_username,
                    "original": original_text,
                    "translated": translated_text,
                    "target_lang": target_lang,
                    "latency": round(latency, 2),
                    "timestamp": time.time()
                }

                await conn.send_json(payload)
            except Exception:
                pass


manager = ConnectionManager()


@app.websocket("/ws/{user}")
async def websocket_endpoint(websocket: WebSocket, user: str):
    await manager.connect(websocket, user)

    try:
        while True:
            data = await websocket.receive_json()

            # User announces language
            if data.get("type") == "set_lang":
                lang = data.get("lang", "en")
                manager.user_lang[user] = lang

                await websocket.send_json({"type": "lang_ack", "lang": lang})
                continue

            # Chat message
            if data.get("type") == "message":
                original_text = data.get("text", "")
                do_translate = data.get("translate", True)

                await manager.broadcast_per_receiver(
                    sender_username=user,
                    original_text=original_text,
                    do_translate=do_translate
                )
                continue

    except WebSocketDisconnect:
        manager.disconnect(websocket)

    except Exception:
        try:
            manager.disconnect(websocket)
        except:
            pass
