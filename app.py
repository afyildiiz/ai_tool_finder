from flask import Flask, request, render_template
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

def find_ai_tool(user_input):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )
        cur = conn.cursor()

        # Kullanıcı girdisindeki anahtar kelimeleri veritabanında ara
        query = f"%{user_input}%"
        cur.execute("""
            SELECT name, description, link FROM ai_tools
            WHERE name ILIKE %s OR description ILIKE %s OR tags ILIKE %s
        """, (query, query, query))

        results = cur.fetchall()
        cur.close()
        conn.close()

        return results

    except Exception as e:
        print(f"Error: {e}")
        return []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form['query']
        tools = find_ai_tool(user_input)

        return render_template('index.html', tools=tools)
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)