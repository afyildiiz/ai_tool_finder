import json
import cohere
from flask import Flask, request, render_template
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY")) # Replace with your actual Cohere API key

app = Flask(__name__)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# AI araçlarını JSON dosyasından yükle
def load_ai_tools_from_json():
    with open('ai_tools.json', 'r') as f:
        return json.load(f)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form['query']

        # AI araçlarını JSON'dan yükle
        all_tools = load_ai_tools_from_json()

        # Kullanıcı girdisindeki anahtar kelimeleri kullanarak araçları filtrele (iyileştirilmiş)
        user_keywords = user_input.lower().split()
        relevant_tools = [tool for tool in all_tools if any(keyword in tool[0].lower() or keyword in tool[1].lower() for keyword in user_keywords)]

        # Cohere ile conversational yanıt oluştur (güncellenmiş)
        if relevant_tools:
            tool_descriptions = "\n".join([f"- **{tool[0]}**: {tool[1]}" for tool in relevant_tools])
            prompt = f"""Kullanıcı {user_input} ile ilgili yapay zeka araçları arıyor. İşte bulduğum bazı araçlar:

{tool_descriptions}
"""
        else:
            prompt = f"Kullanıcı {user_input} ile ilgili yapay zeka araçları arıyor, ancak veritabanımda eşleşen bir araç bulamadım. Kullanıcıya anlayışlı bir şekilde yanıt verin ve belki başka bir arama yapmayı önerebilirsiniz."

        response = co.generate(
            model='command-xlarge-nightly',
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )

        # return render_template('index.html', tools=relevant_tools, conversation=response.generations[0].text)  
        return render_template('conversation.html', tools=relevant_tools, conversation=response.generations[0].text)  # Sadece conversation.html'i döndür

    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)