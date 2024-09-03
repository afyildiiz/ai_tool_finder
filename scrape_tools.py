# githubdaki bir sayfadan ai araçlarını scrape eder ve bu araçları bir psql veritabanına kaydeder

import requests
from bs4 import BeautifulSoup
import psycopg2
import os
from dotenv import load_dotenv
import json

load_dotenv()

# GitHub'dan AI araçlarını çekme fonksiyonu
def scrape_ai_tools():
    url = "https://github.com/mahseema/awesome-ai-tools"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser") # HTML içeriğini BeautifulSoup ile parse eder ve analiz edilebilir hale getirir.

    tools = []
    ul_tags = soup.find_all("ul")
    for ul in ul_tags:
        for li in ul.find_all("li"):
            tool_name = li.text.split(" - ")[0]
            tool_description = li.text.split(" - ")[1] if " - " in li.text else ""
            tool_link = li.find('a')['href'] if li.find('a') else ""
            tools.append((tool_name, tool_description, tool_link))

    return tools


# Veritabanına bağlanma ve AI araçlarını kaydetme fonksiyonu
# def save_tools_to_postgres(tools):
#     try:
#         conn = psycopg2.connect(
#             dbname=os.getenv("POSTGRES_DB"),
#             user=os.getenv("POSTGRES_USER"),
#             password=os.getenv("POSTGRES_PASSWORD"),
#             host=os.getenv("POSTGRES_HOST"),
#             port=os.getenv("POSTGRES_PORT")
#         )
#         cur = conn.cursor()

#         cur.execute("""
#             CREATE TABLE IF NOT EXISTS ai_tools (
#                 id SERIAL PRIMARY KEY,
#                 name TEXT,
#                 description TEXT,
#                 link TEXT,
#                 category TEXT,
#                 tags TEXT
#             );
#         """)

#         for tool_name, tool_description, tool_link in tools: # Scrape edilen her bir AI aracı için aşağıdaki işlemleri yapar:
#             cur.execute("""
#                 INSERT INTO ai_tools (name, description, link)
#                 VALUES (%s, %s, %s)
#             """, (tool_name, tool_description, tool_link))

#         conn.commit()
#         cur.close()
#         conn.close()

#     except Exception as e:
#         print(f"Error: {e}")

def save_tools_to_json(tools):
    """Saves the scraped tools data to a JSON file."""

    with open('ai_tools.json', 'w') as f:
        json.dump(tools, f, indent=4)  # Write data with indentation for readability

# ... (save_tools_to_postgres function)

# Ana program fonksiyonu
if __name__ == "__main__":
    tools = scrape_ai_tools()
    # save_tools_to_postgres(tools)
    save_tools_to_json(tools)  # Call the new function to save to JSON
    print("AI araçları veritabanına ve JSON dosyasına kaydedildi.")
