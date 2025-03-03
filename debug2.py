from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use.agent.views import ActionResult
from browser_use import Agent, Browser, BrowserConfig, BrowserContextConfig
from dotenv import load_dotenv
load_dotenv()

import asyncio
import os

from pydantic import SecretStr, AnyUrl


load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')
# llm = ChatOpenAI(model="gpt-4o")
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key), temperature=0.0)
# sensitive_data={ "name": "testadmin2", "password": "hashedpassword123", "new_password": "hashedpassword123" }

save_screenshots_path = "./task_screenshots_browse-leetpros"

from browser_use.controller.service import Controller
controller = Controller()


urls = []
@controller.registry.action('add URL to list')
def add_url(url: str):
    print("url :", url)
    urls.append(str(url))
    return ActionResult(extracted_content=str(url))

@controller.registry.action('get visited urls list')
def get_url():
    return ActionResult(extracted_content=", ".join(urls), include_in_memory=True)

@controller.registry.action('check if the url already visited')
def check_url(url: str):
    return ActionResult(extracted_content=str(urls.index(url) < 0))


async def main():
    browser = Browser(config=BrowserConfig(
        new_context_config=BrowserContextConfig(
            save_screenshots_path=save_screenshots_path,
            save_recording_path=save_screenshots_path
        )
    ))
    
    agent = Agent(
        task="""Systematically explore https://leetpros.com with these objectives:
1. Start by thoroughly analyzing the homepage content and structure
2. Navigate through all main navigation links (both header and footer menus)
3. Interact with all interactive elements (buttons, dropdowns, tabs) to uncover hidden routes
4. Test form submissions with placeholder data where appropriate
5. Check for dynamic content loaded via AJAX/client-side rendering
6. Document every visited URL using the controller's add_url action
7. Verify comprehensive coverage by ensuring no section remains unexplored
8. Finally, summarize all discovered routes in a report""",
        llm=llm,
        save_screenshots_path=save_screenshots_path,
        browser=browser,
        save_conversation_path="logs/conversation",
        controller=controller
    )
    result = await agent.run()
    # print(result)

asyncio.run(main())