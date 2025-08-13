from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from contextlib import asynccontextmanager

load_dotenv()
from fastapi import HTTPException

graph_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model and build the graph on startup
    global graph_instance
    print("Building agent graph on startup...")
    try:
        graph_builder = GraphBuilder(model_provider="groq")
        graph_instance = graph_builder()
        print("Agent graph built successfully.")
    except Exception as e:
        print(f"Failed to build agent graph: {e}")
    yield
    # Clean up resources if needed on shutdown

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_travel_agent(query:QueryRequest):
    if graph_instance is None:
        raise HTTPException(status_code=503, detail="Agent is not ready. Please check backend logs.")
    try:
        print(query)

        png_graph = graph_instance.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)

        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
        messages={"messages": [query.question]}
        output = graph_instance.invoke(messages["messages"])

        # If result is dict with messages:
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)
        
        return {"answer": final_output}
    except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))