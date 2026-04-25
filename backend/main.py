import os
import time
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Internal Core Imports
from agent.executor import vera_executor
from agent.security import secure_gatekeeper
from agent.tools.reporter import vera_reporter

# --- APP INITIALIZATION ---
app = FastAPI(
    title="V.E.R.A. Neural Core",
    description="Cognitive Backend for JKIAPT (The Hacksmiths)",
    version="3.0.0"
)

# --- CORS CONFIGURATION ---
# Allows your Vercel HUD to communicate with this Render Node
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://vera-agent-frontend.vercel.app", 
        "http://localhost:3000"  # For local debugging
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATA MODELS ---
class AgentRequest(BaseModel):
    instruction: str
    session_id: str = "JKIAPT_ALPHA_01"

# --- API ROUTES ---

@app.get("/")
async def health_check():
    """
    Heartbeat for Render monitoring.
    Returns the system status and node uptime.
    """
    return {
        "status": "OPTIMAL",
        "node": "JKIAPT_PRAYAGRAJ_NODE_01",
        "operator": "Ayush Tripathi",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

@app.post("/run")
async def execute_instruction(request: AgentRequest):
    """
    Primary endpoint for the V.E.R.A. HUD.
    Flow: Security -> Logic -> Execution -> Reporting.
    """
    try:
        # 1. SHIELD LAYER: Intercept and scan for malicious patterns
        # Throws 403 if security protocol is breached
        safe_instruction = secure_gatekeeper(request.instruction)
        
        # 2. NEURAL LAYER: Process the instruction through the Brain
        # This handles planning, tools, and memory internally
        raw_result = await vera_executor.execute(safe_instruction)
        
        # 3. OUTPUT: The executor already returns the formatted report via reporter.py
        return {"logs": raw_result}

    except HTTPException as e:
        # Pass through security or validation errors
        raise e
    except Exception as e:
        # Fallback for unexpected system failures
        print(f"[!] CRITICAL_NODE_FAILURE: {str(e)}")
        error_report = vera_reporter.format_error(str(e))
        return {"logs": error_report}

# --- SERVER STARTUP ---
if __name__ == "__main__":
    import uvicorn
    # Render assigns a dynamic port, default to 10000
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
