import os
import json
from langchain_tavily import TavilySearch
from langchain_google_community import GooglePlacesTool, GooglePlacesAPIWrapper 
from logger.logging import logger 

class GooglePlaceSearchTool:
    def __init__(self, api_key: str):
        self.places_wrapper = GooglePlacesAPIWrapper(gplaces_api_key=api_key)
        self.places_tool = GooglePlacesTool(api_wrapper=self.places_wrapper)
    
    def google_search_attractions(self, place: str) -> dict:
        """
        Searches for attractions in the specified place using GooglePlaces API.
        """
        try:
             return self.places_tool.run(f"top attractive places in and around {place}")
        except Exception as e:
             logger.error(f"Error searching Google attractions for {place}: {e}", exc_info=True)
             return f"Error searching attractions for {place}"
    
    def google_search_restaurants(self, place: str) -> dict:
        """
        Searches for available restaurants in the specified place using GooglePlaces API.
        """
        try:
            return self.places_tool.run(f"what are the top 10 restaurants and eateries in and around {place}?")
        except Exception as e:
            logger.error(f"Error searching Google restaurants for {place}: {e}", exc_info=True)
            return f"Error searching restaurants for {place}"
    
    def google_search_activity(self, place: str) -> dict:
        """
        Searches for popular activities in the specified place using GooglePlaces API.
        """
        try:
            return self.places_tool.run(f"Activities in and around {place}")
        except Exception as e:
            logger.error(f"Error searching Google activities for {place}: {e}", exc_info=True)
            return f"Error searching activities for {place}"

    def google_search_transportation(self, place: str) -> dict:
        """
        Searches for available modes of transportation in the specified place using GooglePlaces API.
        """
        try:
            return self.places_tool.run(f"What are the different modes of transportations available in {place}")
        except Exception as e:
            logger.error(f"Error searching Google transportation for {place}: {e}", exc_info=True)
            return f"Error searching transportation for {place}"

class TavilyPlaceSearchTool:
    def __init__(self):
        pass

    def tavily_search_attractions(self, place: str) -> dict:
        """
        Searches for attractions in the specified place using TavilySearch.
        """
        try:
            tavily_tool = TavilySearch(topic="general", include_answer="advanced")
            result = tavily_tool.invoke({"query": f"top attractive places in and around {place}"})
            if isinstance(result, dict) and result.get("answer"):
                return result["answer"]
            return result
        except Exception as e:
            logger.error(f"Error searching Tavily attractions for {place}: {e}", exc_info=True)
            return f"Error searching attractions for {place}"
    
    def tavily_search_restaurants(self, place: str) -> dict:
        """
        Searches for available restaurants in the specified place using TavilySearch.
        """
        try:
            tavily_tool = TavilySearch(topic="general", include_answer="advanced")
            result = tavily_tool.invoke({"query": f"what are the top 10 restaurants and eateries in and around {place}."})
            if isinstance(result, dict) and result.get("answer"):
                return result["answer"]
            return result
        except Exception as e:
            logger.error(f"Error searching Tavily restaurants for {place}: {e}", exc_info=True)
            return f"Error searching restaurants for {place}"
    
    def tavily_search_activity(self, place: str) -> dict:
        """
        Searches for popular activities in the specified place using TavilySearch.
        """
        try:
            tavily_tool = TavilySearch(topic="general", include_answer="advanced")
            result = tavily_tool.invoke({"query": f"activities in and around {place}"})
            if isinstance(result, dict) and result.get("answer"):
                return result["answer"]
            return result
        except Exception as e:
            logger.error(f"Error searching Tavily activities for {place}: {e}", exc_info=True)
            return f"Error searching activities for {place}"

    def tavily_search_transportation(self, place: str) -> dict:
        """
        Searches for available modes of transportation in the specified place using TavilySearch.
        """
        try:
            tavily_tool = TavilySearch(topic="general", include_answer="advanced")
            result = tavily_tool.invoke({"query": f"What are the different modes of transportations available in {place}"})
            if isinstance(result, dict) and result.get("answer"):
                return result["answer"]
            return result
        except Exception as e:
            logger.error(f"Error searching Tavily transportation for {place}: {e}", exc_info=True)
            return f"Error searching transportation for {place}"
    
