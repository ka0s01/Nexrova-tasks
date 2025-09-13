import os
from fastapi import FastAPI, Form
from fastapi.responses import Response
from dotenv import load_dotenv
from twilio.twiml.messaging_response import MessagingResponse
from fastapi.responses import PlainTextResponse
from supabase import create_client, Client
import google.generativeai as genai


load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

chat_sessions = {}
app = FastAPI()



def get_user(phone: str, name: str = None):
    user = supabase.table("users").select("*").eq("phone", phone).execute()
    if user.data:
        return user.data[0]["id"]
    else:
        new_user = supabase.table("users").insert({"phone": phone, "name": name}).execute()
        return new_user.data[0]["id"]

def add_message(user_id: str, text: str, role: str):
    supabase.table("messages").insert({"user_id": user_id, "message_text": text, "role": role}).execute()

def chat_session(user_id: str):
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])
    return chat_sessions[user_id]



@app.post("/whatsapp")
async def whatsapp_msg_webhook(
    Body: str = Form(...),
    From: str = Form(...),
    ProfileName: str = Form(None)
):
    # print("✅ Incoming message:", Body, "from:", From)

    user_id = get_user(phone=From, name=ProfileName)
    add_message(user_id, Body, "user")
    chat = chat_session(user_id)

    try:
        response = chat.send_message(Body)
        reply_text = response.text
    except Exception as e:
        reply_text = f"error: {str(e)}"

    
    twilio_response = MessagingResponse()
    twilio_response.message(reply_text)

    
    add_message(user_id, reply_text, "AI")

    return PlainTextResponse(str(twilio_response), media_type="application/xml")
