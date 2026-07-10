from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent import AutonomousAgent

app = FastAPI(
    title="Autonomous AI Agent",
    description="Simple AI Agent that plans tasks and generates Word documents.",
    version="1.0.0",
)

agent = AutonomousAgent()


class AgentRequest(BaseModel):
    request: str


@app.get("/")
def root():
    return {
        "message": "Autonomous AI Agent is running!"
    }


@app.post("/agent")
async def run_agent(req: AgentRequest):
    try:
        result = await agent.run(req.request)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )