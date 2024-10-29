# tools.py

from pydantic import BaseModel, Field  # Updated import
from langchain.schema import HumanMessage, SystemMessage  # Updated import
from langchain.tools import tool

from utils.constants import GEMINI

from PIL import Image, ImageDraw, ImageFont
import pyautogui as pg
import base64
import logging

pg.PAUSE = 2

# Rest of your code...


def get_ruled_screenshot():
    try:
        image = pg.screenshot()
    except Exception as ex:
        logging.error(f"Error taking screenshot: {str(ex)}")
        raise

    try:
        # Get the image dimensions
        width, height = image.size

        # Create a new image for the semi-transparent layer
        overlay = Image.new("RGBA", (width, height), (255, 255, 255, 0))  # Transparent layer
        draw = ImageDraw.Draw(overlay)

        # Set the line color (gray) and line opacity (adjusting the alpha value)
        line_color = (200, 200, 0, 128)  # The last value (128) controls opacity, 0 = fully transparent, 255 = fully opaque

        # Load a font for the labels (you can specify any TTF font you have)
        try:
            font = ImageFont.truetype("arial.ttf", 25)
        except IOError:
            font = ImageFont.load_default()

        # Draw vertical and horizontal lines every 50 pixels and add labels
        for x in range(0, width, 50):
            draw.line([(x, 0), (x, height)], fill=line_color, width=1)
            if x % 100 == 0:
                draw.text((x + 5, 5), str(x), font=font, fill=(250, 250, 0, 128))
                draw.text((x, height - 25), str(x), font=font, fill=(250, 250, 0, 128))

        for y in range(0, height, 50):
            draw.line([(0, y), (width, y)], fill=line_color, width=1)
            if y % 100 == 0:
                draw.text((5, y + 5), str(y), font=font, fill=(0, 250, 250, 128))
                text_width, text_height = 35, 15
                draw.text((width - text_width - 5, y + 5), str(y), font=font, fill=(0, 250, 250, 128))

        # Convert screenshot to RGBA for proper merging
        image = image.convert("RGBA")

        # Merge the overlay (with lines and labels) back onto the original image
        combined = Image.alpha_composite(image.convert("RGBA"), overlay)
        combined.save("screenshot.png")
    except Exception as ex:
        logging.error(f"Error processing screenshot: {str(ex)}")
        raise

class ScreenInfo(BaseModel):
    query: str = Field(description="A question about the current screen's status. Should always be in text.")

@tool(args_schema=ScreenInfo)
def get_screen_info(question: str) -> dict:
    """Tool to get information about the current screen based on the user's question. Takes a screenshot with a grid overlay and uses the image to analyze and answer the question."""
    try:
        get_ruled_screenshot()
        with open(f"screenshot.png", "rb") as image_file:
            image = base64.b64encode(image_file.read()).decode("utf-8")
            messages = [
                SystemMessage(
                    content="""You are a Computer agent that analyzes screenshots of the user's screen. Your goal is to verify if any visible changes have occurred on the screen following a command or action. You will analyze the screenshot of the screen with grid lines that help you understand the coordinates.

                            Here's how you can help:
                            1. Identify if a new window, message, or popup is visible.
                            2. Detect if any text, images, or UI elements have changed.
                            3. Find specific coordinates of buttons, text, or areas based on the provided screenshot.
                            4. If there are no visible changes or new elements, respond with 'No changes detected'.

                            Always be precise with coordinates and descriptions, as they will be used for further actions."""
                ),
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": f"{question}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image}"}
                        }
                    ]
                )
            ]
            # Use GEMINI directly for the invocation
            response = GEMINI.invoke(messages)
            return response.content

    except Exception as ex:
        logging.error(f"Error in get_screen_info: {str(ex)}")
        return {"error": str(ex)}
