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

sensitive_data={ "name": "sajeel@mailinator.com" }

save_screenshots_path = "./amplitude-login"


async def main():
    browser = Browser(config=BrowserConfig(
        new_context_config=BrowserContextConfig(
            save_screenshots_path=save_screenshots_path,
            save_recording_path=save_screenshots_path,
            browser_window_size={ 'width': 1980, 'height': 1200 }
        )
    ))
    url = "https://amplitude.com/"
    
    agent = Agent(
        task=f"Goto {url} and login with email and. Use mailinator to check of OTP. then logout.",
        llm=llm,
        sensitive_data=sensitive_data,
        save_screenshots_path=save_screenshots_path,
        browser=browser,
        save_conversation_path="logs/conversation"
    )
    result = await agent.run()
    # print(result)

asyncio.run(main())