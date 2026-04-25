import os
import sys
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- PATH FIX (CRITICAL FOR RENDER) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# --- INTERNAL IMPORTS ---
from agent.executor import vera_executor
from agent.security import secure_gatekeeper, vera_shield
from agent.memory import vera_memory
from tools.reporter import vera_reporter

# --- APP INITIALIZATION ---
app = FastAPI(
    title="V.E.R.A. Neural Core",
    description="Cognitive Backend for JKIAPT (The Hacksmiths)",
    version="3.1.1"
)

# --- STARTUP LOG ---
print("[✓] V.E.R.A Node Initialized Successfully")

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
    session_id: str = "JKIAPT_ALPHA_01"


# --- API ROUTES ---

@app.get("/")
async def health_check():
    return {
        "status": "OPTIMAL",
        "node": "JKIAPT_PRAYAGRAJ_NODE_01",
        "operator": "Ayush Tripathi",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }


@app.post("/run")
async def execute_instruction(request: AgentRequest):
    """
    Flow:
    Security → Planning → Execution → Reporting → Response
    """

    try:
        # 🧹 Normalize input
        instruction = request.instruction.strip()

        # 🔐 1. SECURITY
        safe_instruction = secure_gatekeeper(instruction)

        # 🧠 2. MEMORY CONTROL (prevents context pollution)
        vera_memory.conditional_reset(safe_instruction)

        # ⚙️ 3. EXECUTION
        raw_result = await vera_executor.execute(safe_instruction)

        # 🧹 4. OUTPUT SANITIZATION
        safe_output = vera_shield.filter_output(
            raw_result.get("final_output", "")
        )

        # 📊 5. REPORT GENERATION
        report = vera_reporter.generate_executive_summary(
            instruction=instruction,
            output=safe_output,
            steps=raw_result.get("steps", [])
        )

        # 📦 6. RESPONSE
        return {
            "status": "success",
            "goal": raw_result.get("goal", ""),
            "logs": report,
            "raw": raw_result
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        print(f"[!] CRITICAL_NODE_FAILURE: {str(e)}")

        error_report = vera_reporter.format_error(str(e))

        return {
            "status": "error",
            "logs": error_report
        }


# --- SERVER STARTUP ---
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 10000))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
