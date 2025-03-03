from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig, BrowserContextConfig
from dotenv import load_dotenv
load_dotenv()

import asyncio
import os

from pydantic import SecretStr


load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')
# llm = ChatOpenAI(model="gpt-4o")
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key), temperature=0.0)
# sensitive_data={ "email": "nomantest123@gmail.com", "password": "Noman@12345678"}

save_screenshots_path = "./task_screenshots_appshots_sign-in"





async def main():
    browser = Browser(config=BrowserConfig(
        new_context_config=BrowserContextConfig(
            save_screenshots_path=save_screenshots_path,
            save_recording_path=save_screenshots_path
        )
    ))
    
    agent = Agent(
        task="Goto https://appshots.design/ and login with 'sajeel@mailinator.com'. Use mailinator to check of OTP",
        llm=llm,
        save_screenshots_path=save_screenshots_path,
        browser=browser,
        save_conversation_path="logs/conversation"
    )
    result = await agent.run()
    # print(result)

asyncio.run(main())