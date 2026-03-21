import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from config.settings import settings
from logger.logging import logger
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


class ConfigLoader:
    def __init__(self):
        logger.info(f"Loaded config.....")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self):
        """
        Load and return the LLM model.
        """
        logger.info("LLM loading...")
        logger.info(f"Loading model from provider: {self.model_provider}")
        if self.model_provider == "groq":
            logger.info("Loading LLM from Groq..............")
            groq_api_key = settings.GROQ_API_KEY
            model_name = self.config["llm"]["groq"]["model_name"]
            llm=ChatGroq(model=model_name, api_key=groq_api_key)
            logger.info("LLM loaded successfully from Groq")
        elif self.model_provider == "openai":
            logger.info("Loading LLM from OpenAI..............")
            openai_api_key = settings.OPENAI_API_KEY
            model_name = self.config["llm"]["openai"]["model_name"]
            llm = ChatOpenAI(model_name=model_name, api_key=openai_api_key)
        
        return llm
    