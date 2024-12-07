from aws_requests_auth.aws_auth import AWSRequestsAuth
import json
from datetime import datetime
import requests
import boto3

session = boto3.Session()
credentials = session.get_credentials()

auth = AWSRequestsAuth(aws_access_key=credentials.access_key,
                       aws_secret_access_key=credentials.secret_key,
                       aws_token=credentials.token,
                       aws_host='tmlg7yfb6l.execute-api.us-east-1.amazonaws.com',  
                       aws_region='us-east-1',
                       aws_service='execute-api')

def chatbot_shell():
    """
    A space-themed Martian chatbot shell using API Gateway via boto3.
    """
    print("🪐 Welcome to the Martian Chatbot! 🌌")
    print("👩‍🚀 Type your message below to chat with the Mars Rover. When you're done, type 'exit' to leave the mission.")
    print("🚀 But first, provide an Earth date for your conversation. Expected format: YYYY-MM-DD.\n")

    # Get Earth date from user
    earth_date = ""
    while not earth_date:
        earth_date = input("🗓️ Enter Earth date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(earth_date, "%Y-%m-%d")  # Validate date format
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD.")
            earth_date = ""
    
    print("\n✅ Earth date set to:", earth_date)
    print("You're now connected to the Mars Rover. Let the interplanetary chat begin! 🌠")

    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    conversation_id = current_date

    while True:
        # Read user input
        user_input = input("You 🌍: ").strip()

        # Exit the shell if the user types 'exit'
        if user_input.lower() == "exit":
            print("👋 Goodbye, Earthling! Safe travels through the cosmos! ✨")
            break

        # Prepare the payload
        payload = {
            "user_prompt": user_input,
            "conversation_id": conversation_id,
            "earth_date": earth_date,
        }

        try:
            # Invoke the chatbot API via API Gateway
            response = requests.post('https://tmlg7yfb6l.execute-api.us-east-1.amazonaws.com/Prod/chat', auth=auth, data=json.dumps(payload))

            # Check the response
            if response.status_code == 200:
                print(f"Rover 🛸: {response.text}")  # Customize based on API Gateway response structure
            if response.status_code == 400:
                print("Rover 🚨: Human error. Please check your input and try again.")
            if response.status_code == 429:
                print("Rover 🚨: Space travel is expensive! Please cough up more cash to continue.")
            if response.status_code == 504:
                print("Rover 🚨: Mars is far away. Looks like my answer got lost on the 140 million mile journey.")
            if response.status_code ==500:
                print("Rover 🚨: Houston, we have a problem. Please check my logs.")
            else:
                print("Rover 🚨: Something went wrong. Unable to process your request.")

        except Exception as e:
            print(f"❌ Something went wrong: {e}")
            print("Rover 🚨: Unable to process your request. Please try again.")

if __name__ == "__main__":
    chatbot_shell()