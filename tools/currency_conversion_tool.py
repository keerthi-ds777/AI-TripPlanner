import os
from utils.currency_converter import CurrencyConverter
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()
_api_key = os.environ.get("EXCHANGE_RATE_API_KEY")
_currency_service = CurrencyConverter(_api_key)


@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert an amount from one currency to another. 
    Use ISO 4217 currency codes e.g. USD, EUR, GBP, INR."""
    return _currency_service.convert(amount, from_currency, to_currency)


class CurrencyConverterTool:
    def __init__(self):
        self.currency_converter_tool_list = [convert_currency]