from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()

import asyncio
import os

from pydantic import SecretStr

from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig


load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')
# llm = ChatOpenAI(model="gpt-4o")
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key), temperature=0.0)

save_screenshots_path = "./task_insignia_product_filtering"

url = "https://insignia.com.pk/"





async def main():
    browser = Browser(config=BrowserConfig(
        new_context_config=BrowserContextConfig(
            save_screenshots_path=save_screenshots_path,
            save_recording_path=save_screenshots_path
        ),
        headless=False
    ))
    
    agent = Agent(
        task=f"Goto {url}, search for product and perform product filtering.",
        llm=llm,
        save_screenshots_path=save_screenshots_path,
        browser=browser,
        save_conversation_path="logs/conversation"
    )
    
    await agent.run()

asyncio.run(main())