import os
from google import genai

GEMINI_API_KEY = "AQ.Ab8RN6k19KXOBBEx3A1-HOpaIsRsCFrzNLSUnwzSaQukV3pZA"
client = genai.Client(api_key=GEMINI_API_KEY)






import os
from flask import Flask

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route("/")
def home():
    return "AI Agent is running 24/7 successfully!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

