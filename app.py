import json
import cohere
from flask import Flask, request, render_template
import psycopg2
import os
from dotenv import load_dotenv
from flask_mail import Mail, Message

load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

app = Flask(__name__)

# E-posta yapılandırması
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 465 
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        comment = request.form['text']

        # eposta mesajını oluştur
        msg = Message('Yeni İletişim Formu Gönderimi', sender=email, recipients=[os.environ.get('MAIL_USERNAME')])
        msg.body = f"İsim: {name}\nE-posta: {email}\n\n {comment}"

        # E-postayı gönder
        mail.send(msg)

        feedback= "Message has been sent!"
        return render_template('contact.html', data=feedback)  # data değişkenini gönder

    return render_template('contact.html')

# ai araçlarını json dosyasından yükle
def load_ai_tools_from_json():
    with open('ai_tools.json', 'r') as f:
        return json.load(f)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form['query']

        # ai araçlarını json'dan yükle
        all_tools = load_ai_tools_from_json()

        # kullanıcı girdisindeki anahtar kelimeleri kullanarak araçları filtrele
        user_keywords = user_input.lower().split()
        relevant_tools = [tool for tool in all_tools if any(keyword in tool[0].lower() or keyword in tool[1].lower() for keyword in user_keywords)]

        # cohere ile conversational yanıt oluştur
        if relevant_tools:
            tool_descriptions = "\n".join([f"- **{tool[0]}**: {tool[1]}" for tool in relevant_tools])
            prompt = f"""The user is looking for AI tools related to {user_input}. 
            Respond to the user in an understanding way and perhaps suggest another search.
            Do not list tools

{tool_descriptions}
"""
        else:
            prompt = f"The user is looking for AI tools related to {user_input}, but I couldn't find a matching tool in my database. Respond to the user in an understanding way and maybe you can suggest doing another search."

        response = co.generate(
            model='command-xlarge-nightly',
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
                # yanıtı ilk iki cümle ile sınırla
        conversation_text = response.generations[0].text
        sentences = conversation_text.split('. ')
        limited_conversation = '. '.join(sentences[:2]) + '.' 

        # return render_template('index.html', tools=relevant_tools, conversation=response.generations[0].text)  
        return render_template('conversation.html', tools=relevant_tools, conversation=limited_conversation)  # Sadece conversation.html'i döndür

    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)