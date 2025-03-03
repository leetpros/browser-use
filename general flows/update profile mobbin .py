from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Controller, ActionResult
from browser_use import Agent, Browser, BrowserConfig, BrowserContextConfig
from browser_use.browser.context import BrowserContext
from pathlib import Path
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

sensitive_data={ "name": "testadmin2", "password": os.getenv("PASSWORD"), "new_password": os.getenv("NEW_PASSWORD") }

save_screenshots_path = "./task_screenshots_mobbin_update_profile"

controller = Controller()


@controller.action(
	'Upload file to interactive element with file path ',
)
async def upload_file(index: int, path: str, browser: BrowserContext, available_file_paths: list[str]):
	print(f"Index: {index}")
	print(f"Path: {path}")
	print(f"Available File Paths: {available_file_paths}")
	if path not in available_file_paths:
		return ActionResult(error=f'File path {path} is not available')

	if not os.path.exists(path):
		return ActionResult(error=f'File {path} does not exist')

	dom_el = await browser.get_dom_element_by_index(index)

	file_upload_dom_el = dom_el.get_file_upload_element()

	if file_upload_dom_el is None:
		msg = f'No file upload element found at index {index}'
		return ActionResult(error=msg)

	file_upload_el = await browser.get_locate_element(file_upload_dom_el)
	print(file_upload_el)

	if file_upload_el is None:
		msg = f'No file upload element found at index {index}'
		return ActionResult(error=msg)

	try:
		await file_upload_el.set_input_files(path)
		msg = f'Successfully uploaded file to index {index}'
		return ActionResult(extracted_content=msg, include_in_memory=True)
	except Exception as e:
		msg = f'Failed to upload file to index {index}: {str(e)}'
		return ActionResult(error=msg)





async def main():
    browser = Browser(config=BrowserConfig(
        new_context_config=BrowserContextConfig(
            save_screenshots_path=save_screenshots_path,
            save_recording_path=save_screenshots_path
        )
    ))
    file_path = Path.cwd() / f'files/browser-use.png'
    
    available_file_paths = [str(file_path)]
    print("available_file_paths :", available_file_paths)
    
    agent = Agent(
        task="Goto https://mobbin.com/ and login with 'sajeel@mailinator.com'. Use mailinator to check of OTP. And perform update profile like change name and update profile picture (if option available).",
        llm=llm,
        sensitive_data=sensitive_data,
        save_screenshots_path=save_screenshots_path,
        browser=browser,
        save_conversation_path="logs/conversation",
        available_file_paths=available_file_paths,
        controller=controller
    )
    result = await agent.run()
    # print(result)

asyncio.run(main())