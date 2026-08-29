import os
from flask import Flask, render_template, request, redirect, url_for, session
from google import genai

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

USER_CREDENTIALS = {"admin": "12345"}

AGENTS = {
    "general": {
        "name": "المساعد العام",
        "instruction": "You are a general smart assistant, accurate and fast."
    },
    "physio": {
        "name": "خبير العلاج الطبيعي والتأهيل",
        "instruction": "You are an expert in physical therapy and rehabilitation."
    },
    "accounting": {
        "name": "المحاسب المالي",
        "instruction": "You are an accounting and financial expert."
    },
    "crypto": {
        "name": "خبير تداول العملات الرقمية",
        "instruction": "You are a cryptocurrency trading and market analysis expert."
    }
}

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session['user'] = username
            return redirect(url_for('chat'))
        else:
            error = 'Invalid username or password.'
    return render_template('login.html', error=error)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    bot_response = None
    user_message = None
    selected_agent = request.form.get('agent', 'general') if request.method == 'POST' else 'general'

    if request.method == 'POST' and 'message' in request.form and request.form['message'].strip():
        user_message = request.form['message']
        agent_info = AGENTS.get(selected_agent, AGENTS['general'])
        
        try:
            prompt = f"System Instruction: {agent_info['instruction']}\n\nUser Question: {user_message}"
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            bot_response = response.text
        except Exception as e:
            bot_response = f"Error: {str(e)}"
        
    return render_template('chat.html', username=session['user'], response=bot_response, user_message=user_message, agents=AGENTS, 
selected_agent=selected_agent)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

