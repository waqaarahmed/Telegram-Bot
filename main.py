from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = 'your-openai-api-key-here'  # Replace with your actual OpenAI API key

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    # Get the message from WhatsApp
    incoming_msg = request.values.get('Body', '').strip()
    
    # Initialize an empty reply message
    bot_reply = "I couldn't understand that. Could you please try again?"

    # Only generate a response if a message was received
    if incoming_msg:
        try:
            # Send the user's message to the OpenAI API
            response = openai.Completion.create(
                engine="text-davinci-003",   
                prompt=incoming_msg,         
                max_tokens=100,              
                n=1,                         
                stop=None,                   
                temperature=0.7              
            )

            # Get the text of the response from OpenAI API
            bot_reply = response.choices[0].text.strip()

        except Exception as e:
            # If something goes wrong, provide a default response
            bot_reply = "Oops! I couldn't process your request at the moment. Try again later."

    # Create a Twilio response object
    resp = MessagingResponse()
    
    # Add the OpenAI-generated reply to the Twilio message
    resp.message(bot_reply)

    return str(resp)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
