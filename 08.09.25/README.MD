## Setup Instructions
- Clone the Repo
- Create a virtual environment and activate it
  ``` bash
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- Install the dependancies
  ``` bash
  pip install -r requirements.txt
  ```
- Create .env file
  ``` bash
  GOOGLE_API_KEY=your_gemini_api_key
  SUPABASE_URL=your_supabase_project_url
  SUPABASE_KEY=your_supabase_anon_or_service_key

  ```
- Create the tables in Supabase
- Run the FastAPI server
  ``` bash
  uvicorn main:app --reload --host 0.0.0.0 --port 8000

  ```
- Expose the server to ngrok
  ``` bash
  ngrok http 8000

  ```
- Configure the Twilio Sandbox
- Set the webhook URL (ngrok forwarding)
- Message Twilio on whatsapp
