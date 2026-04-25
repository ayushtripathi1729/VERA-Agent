import os
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Internal Imports
from agent.executor import run_agent
from agent.security import secure_gatekeeper

# --- API INITIALIZATION ---
app = FastAPI(
    title="V.E.R.A. Neural Core",
    description="Cognitive Backend for JKIAPT (The Hacksmiths)",
    version="3.0.0"
)

# --- CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://vera-agent-frontend.vercel.app", 
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATA MODELS ---
class AgentRequest(BaseModel):
    instruction: str
    session_id: str = "default_user"

# --- ROUTES ---
@app.get("/")
async def health_check():
    """System heartbeat for Render monitoring."""
    return {
        "status": "ONLINE",
        "node": "JKIAPT_PRAYAGRAJ",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/run")
async def execute_instruction(request: AgentRequest):
    try:
        # 1. Security Gatekeeper
        safe_instruction = secure_gatekeeper(request.instruction, request.session_id)
        
        # 2. Neural Executor
        logs = await run_agent(safe_instruction)
        
        return {"logs": logs}

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"[!] CRITICAL_SYSTEM_ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"NEURAL_CORE_FAILURE: {str(e)}")

# --- SERVER STARTUP ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
