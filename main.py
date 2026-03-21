from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
import os
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from pydantic import BaseModel
from contextlib import asynccontextmanager
from config.settings import settings
from logger.logging import logger

load_dotenv() # Handled by settings.py
from fastapi import HTTPException

graph_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model and build the graph on startup
    global graph_instance
    logger.info("Building agent graph on startup...")
    try:
        graph_builder = GraphBuilder(model_provider="groq")
        graph_instance = graph_builder()
        logger.info("Agent graph built successfully.")
    except Exception as e:
        logger.error(f"Failed to build agent graph: {e}", exc_info=True)
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
        logger.info(f"Received query: {query.question}")

        try:
            png_graph = graph_instance.get_graph().draw_mermaid_png()
            with open("my_graph.png", "wb") as f:
                f.write(png_graph)
                logger.info(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
        except Exception as e:
            logger.warning(f"Could not save graph image: {e}")

        
        messages={"messages": [HumanMessage(content=query.question)]}
        output = await graph_instance.ainvoke(messages)

        # If result is dict with messages:
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)
        
        return {"answer": final_output}
    except Exception as e:
       logger.error(f"Error processing query: {e}", exc_info=True)
       raise HTTPException(status_code=500, detail=str(e))