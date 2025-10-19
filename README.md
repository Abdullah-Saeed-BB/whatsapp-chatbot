# Whatsapp Chatbot
Intelligent Whatsapp chatbot built using **Flask** and **Twilio API** to connect the server to the whatsapp, and **Gemini model**.<br/>
The chatbot answers for CreativeCut e-learning platofrm supporting English and Arabic, and display customer subscription details using the subscription ID.

I made an **[web application](WEB_APPLICATION)** to tune the **Chatbot model**.
#### [Whatsapp Chatbot (Send `join map-recognize`)](WHATSAPP_CHATBOT)
## Project Structure
#### Chat Bot:
 - `routes/utils.py`: Functions for loading the converstion, saving them temprorliey, load the offers, and convert the *system_instruction.json* to text.
 - `routes/whatsapp.py`: Contain the route for reciving & sending whatsapp messages.
 - `db/system_instruction.json`: Contain the main points of system instruciton to give to the Gemini model to instrict to it (It get convert to text before feed it to the model). 
#### Web Application:
 - `routes/auth.py`: Log in page, before entering the dashbaord.
 - `routes/chatbot_instruction.py`: Here were the admin can access to the *system_instruction* and update it.
 - `routes/customers.py`: Shows all the customers data.
 - `routes/dashbaord.py`: Dashboard page
 - `routes/offers.py`: Shows all the offers and updating them.
 - `routes/subscription.py`: Form for submission the subscription.
 - `templates`: Contain all the HTML files.
 - `static`: Contain all the CSS files.
 - `db/creativecut.db`: Is the database for the CreativeCut platform, (tables: customers, and offers)
 - `db/schema.sql`: Is SQL code to apply the schema to the database.

## Installation

**1. Install dependencies:** <br/>

```
pip install -r requirements.txt
```

**2. Create an .env file:** <br/>
Add your environment variables:<br/>

```
SECRET_KEY=any_random_string
GEMINI_API_KEY=your_gemini_api_key
ACCOUNT_SID=your_twilio_account_sid
AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUM=your_twilio_whatsapp_number
```

**3. Get your Gemini API key:** <br/>
Go to Google AI Studio → Click Get Started or sign in → Scroll down to View API keys → Create API key, if prompted, create a new project.

Copy your API key and add it to .env as `GEMINI_API_KEY`.

**4. Test locally:** <br/>
To test the model before going any deeper, run the `main.py`:
```
python main.py
```

Test the endpoint using Postman:

- **Method:** POST
- **URL:** http://localhost:5000/whatsapp
- **Body:** `form-data` with key _Body_ and your message as the _value_.

You will get the result in XML.

**5. Set up Twilio Sandbox for WhatsApp:** <br/>
Go to Twilio → Sign in → Navigate to Twilio Console → Go to Messaging → Try it out → Send a WhatsApp message.

Initialize the Sandbox (you'll get a phone number and join code).

In your Account Dashboard, copy your Account SID and Auth Token and add them to .env.

**6. Expose your local server (using ngrok):**

```
pip install pyngrok
```

```
ngrok http 5000
```

Copy the Forwarding URL and paste it in Twilio:
Messaging → Send a WhatsApp Message → Sandbox settings → When a message comes in

Remeber to add `/whatsapp` in the end of the URL<br/>
(e.g. https://your-ngrok-url.ngrok.io/whatsapp)

Start chatting<br/>
Send the join code to the WhatsApp sandbox number<br/>
Then send any message — your model should respond automatically.

## Screenshot
![Chatbot_whatsappjpg](https://github.com/user-attachments/assets/26f6fa3a-39b2-493a-b97c-b7469df98616)
