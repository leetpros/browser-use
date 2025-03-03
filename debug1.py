# import asyncio
# from browser_use import Browser, BrowserConfig
# from browser_use.dom.service import DomService

# async def debug_element_finding():
#     browser = Browser(config=BrowserConfig(headless=False))
    
#     async with await browser.new_context() as context:
#         page = await context.get_current_page()
#         await page.goto('https://www.google.com')
        
#         # Get browser state which includes selector map
#         state = await context.get_state()
        
#         # Print selector map object and its keys to see available indices
#         print("\nSelector Map Object:")
#         print(state.selector_map)
#         print("\nSelector Map Keys (Available Indices):")
#         print(list(state.selector_map.keys()))
        
#         # Print all found elements with their indices
#         print("\nFound Interactive Elements:")
#         print(state.element_tree.clickable_elements_to_string())
        
#         # Try to get a valid index from the selector map
#         if state.selector_map:
#             valid_index = list(state.selector_map.keys())[0]
#             print(f"\nTrying to find element with index {valid_index}")
            
#             # Get element using state's selector map
#             element_node = state.selector_map[valid_index]
#             element = await context.get_locate_element(element_node)
            
#             if element:
#                 print(f"Found element:")
#                 print(f"Tag: {await element.evaluate('el => el.tagName')}")
#                 print(f"Text: {await element.text_content()}")
                
#                 # Try to click it
#                 try:
#                     await element.click()
#                     print("Successfully clicked element")
#                 except Exception as e:
#                     print(f"Failed to click element: {e}")
#             else:
#                 print("Could not locate element")
                
#             # Print details about the element we tried to find
#             print("\nElement Details:")
#             print(f"Tag: {element_node.tag_name}")
#             print(f"XPath: {element_node.xpath}")
#             print(f"Attributes: {element_node.attributes}")
#             print(f"Is Interactive: {element_node.is_interactive}")
#             print(f"Is Visible: {element_node.is_visible}")
            
#         else:
#             print("No interactive elements found!")
        
#         input("Press Enter to close browser...")

# if __name__ == "__main__":
#     asyncio.run(debug_element_finding())



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
# sensitive_data={ "name": "testadmin2", "password": "hashedpassword123", "new_password": "hashedpassword123" }

save_screenshots_path = "./task_screenshots_booking_com"





async def main():
    browser = Browser(config=BrowserConfig(
        new_context_config=BrowserContextConfig(
            save_screenshots_path=save_screenshots_path,
            save_recording_path=save_screenshots_path
        )
    ))
    
    agent = Agent(
        task="Goto https://booking.com and sign-up with dummy email and password. And for dummy email, use mailinator and use email 'sajeel@mailinator.com'.",
        llm=llm,
        save_screenshots_path=save_screenshots_path,
        browser=browser,
        save_conversation_path="logs/conversation"
    )
    result = await agent.run()
    # print(result)

asyncio.run(main())