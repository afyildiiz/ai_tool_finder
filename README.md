pip install -r requirements.txt

if os mac : source venv/bin/activate
else : venv/bin/activate

gunicorn -w 4 app:app
