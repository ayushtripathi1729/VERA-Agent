import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent.executor import run_agent
from agent.security import secure_gatekeeper

# --- API INITIALIZATION ---

app = FastAPI(
    title="V.E.R.A. Neural Core",
    description="Cognitive Backend for The Hacksmiths (JKIAPT)",
    version="3.0.0"
)

# --- CORS CONFIGURATION ---
# This allows your specific Vercel frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://vera-agent-frontend.vercel.app", # Update this with your actual Vercel URL
        "http://localhost:3000"                  # For local development
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
        "timestamp": os.popen("date").read().strip()
    }

@app.post("/run")
async def execute_instruction(request: AgentRequest):
    """
    The primary endpoint for the V.E.R.A. HUD.
    Includes security screening and agentic execution.
    """
    try:
        # 1. Pass through Security Gatekeeper
        safe_instruction = secure_gatekeeper(request.instruction, request.session_id)
        
        # 2. Trigger the Neural Executor
        # This calls Planner -> Tools -> Reporter internally
        logs = await run_agent(safe_instruction)
        
        return {"logs": logs}

    except HTTPException as e:
        # Pass through rate-limit or security exceptions
        raise e
    except Exception as e:
        # Catch-all for internal failures
        print(f"[!] CRITICAL_SYSTEM_ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="NEURAL_CORE_FAILURE")

# --- SERVER STARTUP ---
if __name__ == "__main__":
    import uvicorn
    # Use the port assigned by Render, defaulting to 10000
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
