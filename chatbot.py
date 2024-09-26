# chatbot.py

def get_chatbot_response(user_message):
    responses = {
        "hello": "Hello! How can I help you today?",
        "help": "Sure, I'm here to assist you. You can ask me about our products or your order.",
        "price": "All our products are reasonably priced. You can check the product page for detailed pricing.",
        "thank you": "You're welcome! Let me know if you need anything else.",
        "bye": "Goodbye! Have a great day!"
    }
    
    # Normalize user message to lowercase
    user_message = user_message.lower()

    # Return a response if the message matches predefined responses
    for key in responses:
        if key in user_message:
            return responses[key]
    
    # Default response
    return "I'm sorry, I didn't understand that. Can you please rephrase?"