import time
from datetime import datetime
from typing import Dict, Any, List
from agent import initialize_vera_agent

# Initialize the global agent instance
# We do this at the module level for faster subsequent calls (warm start)
vera_executor = initialize_vera_agent()

class NeuralExecutor:
    """
    Handles the execution logic for V.E.R.A.
    Translates raw LLM output into a format compatible with the Frontend Terminal.
    """

    @staticmethod
    async def run(instruction: string) -> List[Dict[str, Any]]:
        logs = []
        
        # 1. Initialize Neural Link Log
        logs.append({
            "message": "Neural link established. Injecting instruction...",
            "status": "SYSTEM",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })

        try:
            # 2. Execute via LangChain
            start_time = time.time()
            
            # Note: We use ainvoke for asynchronous execution to keep FastAPI responsive
            response = await vera_executor.ainvoke({"input": instruction})
            
            execution_time = round(time.time() - start_time, 2)
            output = response.get("output", "Empty response from neural core.")

            # 3. Success Log
            logs.append({
                "message": f"Execution complete in {execution_time}s.",
                "status": "SUCCESS",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })

            # 4. Final Result Log
            logs.append({
                "message": output,
                "status": "INFO",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })

        except Exception as e:
            # 5. Fail-Safe Error Handling
            # This ensures the backend doesn't crash, it just reports the error to the HUD
            error_detail = str(e)
            logs.append({
                "message": f"CRITICAL_FAILURE: {error_detail}",
                "status": "ERROR",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            # Log to server console for debugging
            print(f"[!] AGENT ERROR: {error_detail}")

        return logs

# Export the runner function
async def run_agent(instruction: str):
    return await NeuralExecutor.run(instruction)
