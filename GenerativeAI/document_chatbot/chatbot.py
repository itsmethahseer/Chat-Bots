# Import Palm library
from google.cloud import aiplatform

# Create Palm Predictor client
palm_predictor = aiplatform.Predictor(client=aiplatform.getClient())

# Define user prompt for chatbot
user_prompt = "What is the Thahseer's graduation."

# Send prompt to Palm model and get response
palm_response = palm_predictor.predict(instances={"text": user_prompt})

# Extract and display chatbot response
chatbot_response = palm_response["predictions"][0]
print(f"Chatbot: {chatbot_response}")
