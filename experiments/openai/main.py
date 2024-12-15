import openai
import os
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_image(image_path):
    try:
        # Load the image file and encode it in base64
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
        return image_data
    except  Exception as e:
        print('Error in image_path loading', e)

def classify_food_and_get_macros(image_path):
    """
    Classify food items in an image and predict their macros and calories using OpenAI GPT-4 Vision.

    Args:
        image_path (str): Path to the image file to be analyzed.

    Returns:
        dict: A dictionary containing the classified food items and their predicted macros and calories.
    """
    try:
        client = openai.OpenAI(
            api_key=os.getenv("OPENAI_KEY")
        )
        print(f"Current working directory: {os.getcwd()}")

        # Load the image file
        encoded_string = load_image(image_path)

        # Define the prompt
        prompt = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Classify the food items in this image and estimate their macros (protein, fat, carbs) and calories."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_string}"}} # Adjust MIME type if needed
                ],
            }
        ]

        # Make the API call
        response = client.chat.completions.create(
            model= os.getenv("MODEL"),
            messages=prompt
        )

        # Parse and return the response
        result = response.choices[0].message.content
        return result

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Load API key from environment variable
    openai.api_key = os.getenv("OPENAI_KEY")

    if not openai.api_key:
        print("API key is missing. Please check your .env file.")
    else:
        # Example usage
        image_path = r"data\20151221132515.jpg"  # Replace with your image file path
        result = classify_food_and_get_macros(image_path)

        if result:
            print("Food classification and macros:")
            print(result)
        else:
            print("Failed to get classification and macros.")