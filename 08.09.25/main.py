import requests
from fastapi import FastAPI, Form,Request
import os
from dotenv import load_dotenv
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse

import google.generativeai as genai
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])


app = FastAPI()

def send_response(User_Message : str)-> str:
    return f"user message: {User_Message}"


@app.post("/whatsapp")
async def whatsapp_msg_webhook(Body : str = Form(...)):
    # Response_msg = send_response(Body)
    # return PlainTextResponse(Response_msg)

    try:
        response = chat.send_message(Body)
        twillio_response = MessagingResponse()
        twillio_response.message(response.text)
        return PlainTextResponse(str(twillio_response),media_type="application/xml")
    except Exception as e:
        twillio_response = MessagingResponse()
        twillio_response.message(f"error: {str(e)}")
        return PlainTextResponse(str(twillio_response),media_type="application/xml")

    




