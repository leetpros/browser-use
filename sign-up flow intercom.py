from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig, BrowserContextConfig
from dotenv import load_dotenv
load_dotenv()

import asyncio
import os
from pathlib import Path
from pydantic import SecretStr

# Import the function from our new script
from save_unique_focus_images import save_unique_focus_images


load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError('GEMINI_API_KEY is not set')

password = os.getenv('INTERCOM_PASSWORD')
if not password:
    raise ValueError('INTERCOM_PASSWORD is not set')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key), temperature=0.0)

sensitive_data = { "email": "sajeel1@mailinator.com", "password": password }

save_screenshots_path = "./intercom-sign-up-1"


async def main():
    browser = Browser(config=BrowserConfig(
        new_context_config=BrowserContextConfig(
            save_screenshots_path=save_screenshots_path,
            save_recording_path=save_screenshots_path,
            browser_window_size={ 'width': 1980, 'height': 1200 }
        )
    ))
    url = "https://www.intercom.com/"
    
    agent = Agent(
        task=f"Goto {url} and sign-up using email and password. Use mailinator to check of OTP. then logout.",
        llm=llm,
        sensitive_data=sensitive_data,
        save_screenshots_path=save_screenshots_path,
        browser=browser,
        save_conversation_path="logs/conversation"
    )
    result = await agent.run()
    
    # After agent run completes, save unique focus images
    print("Agent run completed. Saving unique focus images...")
    unique_images_dir = save_unique_focus_images(save_screenshots_path)
    if unique_images_dir:
        print(f"Unique focus images saved to: {unique_images_dir}")
    else:
        print("No unique focus images were found or an error occurred")

asyncio.run(main())