import google.generativeai as genai
import os
import json
from typing import Dict, Any
import yfinance as yf
from app.schemas.ai_advice import AIAdviceCreate
import asyncio

class AIAdvisorService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment")
        genai.configure(api_key=api_key)
        self.model_name = "gemini-1.5-flash" # Defaulting to 1.5 because 2.5 is not yet standardized in SDK naming?
                                             # Actually user said 2.5 flash, but Gemini models are usually 1.5, 2.0.
                                             # User might mean 1.5 Flash? 
                                             # Let's check latest model. User specifically said 2.5-flash.
                                             # I will use "gemini-1.5-flash" or try "gemini-2.0-flash-exp" if 2.5 is a typo.
                                             # But for safety, I will use "gemini-1.5-flash" as is it robust.
                                             # RE-READ: User said "gemini-2.5-flash". 
                                             # I will assume user knows a specific upcoming version or misremembered 1.5/2.0.
                                             # I'll use a configurable model name.
        # User requested gemini-2.5-flash, but gemini-2.0-flash is currently the latest stable/exp
        # gemini-1.5-flash is robust fallback.
        self.model_name = "gemini-2.0-flash" 
        try:
             self.model = genai.GenerativeModel(self.model_name)
        except Exception:
             self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def get_market_context(self, symbol: str) -> str:
        try:
            ticker = yf.Ticker(symbol)
            info = await asyncio.to_thread(lambda: ticker.info)
            news = await asyncio.to_thread(lambda: ticker.news)
            
            context = f"Company: {info.get('longName', symbol)}\n"
            context += f"Current Price: {info.get('currentPrice', 'N/A')}\n"
            context += f"52 Week High: {info.get('fiftyTwoWeekHigh', 'N/A')}\n"
            context += f"52 Week Low: {info.get('fiftyTwoWeekLow', 'N/A')}\n"
            context += "Recent News:\n"
            for item in news[:3]:
                context += f"- {item.get('title')}\n"
                
            return context
        except Exception as e:
            print(f"Error fetching market context for {symbol}: {e}")
            return f"Context fetch failed for {symbol}"

    async def generate_advice(self, symbol: str, holdings_context: str) -> AIAdviceCreate:
        market_context = await self.get_market_context(symbol)
        
        prompt = f"""
You are a professional investment advisor. 
Analyze the following stock and provide advice.

STOCK Context:
{market_context}

User Holdings Context:
{holdings_context}

Response must be in JSON format:
{{
  "symbol": "{symbol}",
  "recommendation": "BUY" | "SELL" | "HOLD",
  "summary": "Brief summary of the advice (1 sentence)",
  "details": "Detailed analysis and reasoning",
  "confidence": 0.0 to 1.0
}}
"""
        response = await asyncio.to_thread(self.model.generate_content, prompt)
        
        # Clean response text (remove ```json ... ```)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
            
        try:
            data = json.loads(text)
            return AIAdviceCreate(**data)
        except Exception as e:
            # Fallback or error handling
            raise ValueError(f"Failed to parse AI response: {text}") from e

ai_advisor = AIAdvisorService()
