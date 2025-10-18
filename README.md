# Whatsapp Chatbot
Intelligent Whatsapp chatbot built using **Flask** and **Twilio API** to connect the server to the whatsapp, and **Gemini model**.<br/>
The chatbot answers for CreativeCut e-learning platofrm supporting English and Arabic, and display customer subscription details using the subscription ID.

I made an **[web application](WEB_APPLICATION)** to tune the **Chatbot model**.
#### [Whatsapp Chatbot (Send `join map-recognize`)](WHATSAPP_CHATBOT)
## Project Structure
#### Chat Bot:
 - `routes/utils.py`: Contain these functions: loading the converstion and saving them temprorliey, and load the offers and convert the *system_instruction.json* to text.
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
[Process for getting the Gemini Keys and Twilio Keys]

## Screenshots
