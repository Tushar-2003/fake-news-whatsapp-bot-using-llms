from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

ollama = Ollama(base_url='http://localhost:11434',
model="llama2")
app = Flask(__name__)

template = """is the information true or false, also give a detailed explanation of it not being true/false.
information is: {news}
"""
def get_fact_check_response(news):
  prompt_template = PromptTemplate.from_template(template=template)
  filled_prompt = prompt_template.format(news=news)
  generated_info = ollama.invoke(filled_prompt)
  return generated_info

@app.route("/sms", methods=['GET', 'POST'])
def sms():
    incoming_message_body = request.values.get('Body', '').lower()

    response = MessagingResponse()
    if incoming_message_body == "hi":
        response.message("hi, I can help you check the truthfulness of news headlines. Just send me the headline!")  # Create a response message directly within the TwiML response
    else:
        news = incoming_message_body
        response.message(get_fact_check_response(news))


    return str(response)  # Return the TwiML response

if __name__ == "__main__":
    app.run(debug=True)
