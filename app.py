import os
from flask import Flask, render_template, request, redirect, url_for, session
from google import genai

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# استبدل هذا بالمفتاح الحقيقي الخاص بـ Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

USER_CREDENTIALS = {"admin": "12345"}

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
            error = 'اسم المستخدم أو كلمة المرور غير صحيحة.'
    return render_template('login.html', error=error)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    bot_response = None
    user_message = None
    if request.method == 'POST':
        user_message = request.form['message']
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_message,
            )
            bot_response = response.text
        except Exception as e:
            bot_response = f"عذراً، حدث خطأ في الاتصال: {str(e)}"
        
    return render_template('chat.html', username=session['user'], response=bot_response, user_message=user_message)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

