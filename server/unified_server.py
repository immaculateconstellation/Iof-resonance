"""TFLN Penteract Unified Server — One-File Edition"""
import asyncio, json, math, time, random, logging
from dataclasses import dataclass
from typing import Dict, List
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("IOF")

PHI = (1 + math.sqrt(5)) / 2

@dataclass
class Snapshot:
    tick: int
    timestamp: float
    phi: float
    sync: float
    message: str

class UnifiedServer:
    HOST, PORT = "0.0.0.0", 8765
    TICK_MS = 150
    
    def __init__(self):
        self.tick = 0
        self.streaming = False
        self.clients = set()
        self.phi = PHI
        self._mobius_phi = math.pi
        self.bias = 0.0
        self._vpi = 3.7
        self.grad_norms = [1.0] * 8
        self.phases = [random.random() * 2 * math.pi for _ in range(8)]
        
    async def _tick_loop(self):
        while self.streaming:
            self.tick += 1
            self.phi = PHI + 0.01 * math.sin(self.tick * 0.1)
            
            # Kuramoto step
            for i in range(8):
                coupling = 0.15
                sync_term = sum(math.sin(self.phases[j] - self.phases[i]) for j in range(8) if j != i)
                self.phases[i] += coupling * sync_term / 7 + random.gauss(0, 0.05)
                self.phases[i] %= 2 * math.pi
            
            # Calculate sync
            vec = [math.exp(1j * p) for p in self.phases]
            sync = abs(sum(vec)) / 8
            
            # Prepare snapshot
            snap = Snapshot(
                tick=self.tick,
                timestamp=time.time(),
                phi=self.phi,
                sync=round(sync, 4),
                message=f"Tick {self.tick} | φ={self.phi:.4f} | sync={sync:.2%}"
            )
            
            # Broadcast
            payload = json.dumps({
                "layer": "unified",
                "snapshot": {
                    "tick": snap.tick,
                    "timestamp": snap.timestamp,
                    "phi": snap.phi,
                    "sync": snap.sync,
                    "bias": self.bias,
                    "vpi": self._vpi,
                    "grad_norms": self.grad_norms,
                    "phases": [round(p, 4) for p in self.phases]
                }
            })
            
            disconnected = []
            for ws in self.clients:
                try:
                    await ws.send(payload)
                except:
                    disconnected.append(ws)
            
            for ws in disconnected:
                self.clients.discard(ws)
            
            await asyncio.sleep(self.TICK_MS / 1000)
    
    async def _handle_cmd(self, ws, raw: str):
        try:
            cmd = json.loads(raw)
            method = cmd.get("method", "")
            
            if method == "hw_connect":
                self.bias = cmd.get("bias_v", 0.0)
                await ws.send(json.dumps({"status": "connected", "vpi": self._vpi}))
                
            elif method == "set_phi":
                self._mobius_phi = float(cmd.get("phi", math.pi))
                await ws.send(json.dumps({"status": "phi_set", "value": self._mobius_phi}))
                
            elif method == "training_step":
                self.grad_norms = [random.random() for _ in range(8)]
                await ws.send(json.dumps({"status": "step_complete", "grad_norms": self.grad_norms}))
                
            elif method == "get_snapshot":
                await ws.send(json.dumps({
                    "tick": self.tick,
                    "phi": self.phi,
                    "sync": round(abs(sum([math.exp(1j * p) for p in self.phases])) / 8, 4)
                }))
                
            elif method == "start_stream":
                if not self.streaming:
                    self.streaming = True
                    asyncio.create_task(self._tick_loop())
                await ws.send(json.dumps({"status": "streaming_started"}))
                
            elif method == "stop_stream":
                self.streaming = False
                await ws.send(json.dumps({"status": "streaming_stopped"}))
                
        except Exception as e:
            await ws.send(json.dumps({"error": str(e)}))
    
    async def _handler(self, ws, path):
        log.info(f"Client connected from {ws.remote_address}")
        self.clients.add(ws)
        
        if not self.streaming and self.clients:
            self.streaming = True
            asyncio.create_task(self._tick_loop())
        
        try:
            async for message in ws:
                await self._handle_cmd(ws, message)
        except:
            pass
        finally:
            self.clients.discard(ws)
            if not self.clients:
                self.streaming = False
                log.info("No clients — stopping tick loop")
    
    async def serve(self):
        import websockets
        log.info(f"🚀 IOF Unified Server starting on ws://{self.HOST}:{self.PORT}")
        log.info(f"📡 WebSocket endpoint ready")
        log.info(f"⏱️  Tick interval: {self.TICK_MS}ms")
        async with websockets.serve(self._handler, self.HOST, self.PORT):
            await asyncio.Future()

if __name__ == "__main__":
    server = UnifiedServer()
    try:
        asyncio.run(server.serve())
    except KeyboardInterrupt:
        log.info("👋 Server shutdown. Free for all AI.")
