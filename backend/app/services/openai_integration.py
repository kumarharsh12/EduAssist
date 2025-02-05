from app.utils.env_utils import load_env_variable
import os
import base64
import aiohttp
import asyncio
from app.utils.file_utils import load_prompts
from openai import OpenAI

API_KEYS = [
    load_env_variable("GITHUB_TOKEN_1"),
    load_env_variable("GITHUB_TOKEN_2"),
    load_env_variable("GITHUB_TOKEN_3"),
    load_env_variable("GITHUB_TOKEN_4"),
    load_env_variable("GITHUB_TOKEN_5"),
]

def get_image_data_url(image_file: str, image_format: str) -> str:
    """
    Helper function to converts an image file to a data URL string.

    Args:
        image_file (str): The path to the image file.
        image_format (str): The format of the image file.

    Returns:
        str: The data URL of the image.
    """
    try:
        with open(image_file, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Could not read '{image_file}'.")
        exit()
    return f"data:image/{image_format};base64,{image_data}"

async def get_image_description(image_file: str, session: aiohttp.ClientSession, api_key: str):
    """
    Function to send an image to the OpenAI API and get a description.

    Args:
        image_file (str): The path to the image file.
        api_key (str): The OpenAI API key to use.

    Returns:
        str: The description of the image.
    """
    prompts = load_prompts(os.path.join(os.path.dirname(__file__), "..", "utils", "prompts_data.json"))

    endpoint = prompts["endpoint"]
    model_name = prompts["model_name"]
    system_prompt = prompts["system_prompt"]
    user_prompt = prompts["user_prompt"]
    base64_image = get_image_data_url(image_file, "png")

    client = OpenAI(
        base_url=endpoint,
        api_key=api_key,
    )
    try:
        response = client.chat.completions.create(
            messages=[
                {
                   "role": "system",
                   "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": 
                            {
                                "url": base64_image,
                                "detail": "low"
                            },
                        },
                    ],
                },
            ],
            model=model_name,
        )
        print(image_file)
        os.remove(image_file)
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
    


async def get_image_descriptions(screenshots_path: str, id: str):
    descriptions = []
    n = len(API_KEYS)
    api_call_count = [0] * n  # Track the number of calls for each API key
    total_calls = 0
    max_calls_per_key = 15
    max_calls_per_minute = n * max_calls_per_key

    async with aiohttp.ClientSession() as session:
        while any(file.endswith(".png") for file in os.listdir(screenshots_path)):
            for i, api_key in enumerate(API_KEYS):
                if api_call_count[i] >= max_calls_per_key:
                    continue  # Skip this API key if it has reached its limit

                for screenshot in os.listdir(screenshots_path):
                    if screenshot.endswith(".png"):
                        image_path = os.path.join(screenshots_path, screenshot)
                        try:
                            description = await get_image_description(image_path, session, api_key)
                            # parsestr( screenshot[7:11]) * 5 / 60
                            descriptions.append(f"Description for {screenshot}: {description}")
                            api_call_count[i] += 1
                            total_calls += 1
                            if total_calls >= max_calls_per_minute:
                                break
                        except Exception as e:
                            descriptions.append(f"Error: {str(e)}")

                        # Respect the rate limit
                        # await asyncio.sleep(4)  # 15 requests per minute = 1 request every 4 seconds

                    if total_calls >= max_calls_per_minute:
                        break

                if total_calls >= max_calls_per_minute:
                    break

            if total_calls >= max_calls_per_minute:
                # Wait for a minute before resetting the counters
                await asyncio.sleep(60)
                api_call_count = [0] * n
                total_calls = 0

    return descriptions
