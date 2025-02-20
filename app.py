from flask import Flask, render_template, request
import openai
import os
import random
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# List of random French words
french_words = ["baguette", "croissant", "fromage", "bonjour", "même", "s'il vous plaît", "merde", "voilà", "déjà vu"]

def inject_french(text):
    """Inject random French words into the response"""
    words = text.split()
    for i in range(0, len(words), random.randint(3, 6)):  # Every 3-6 words, insert a French word
        words.insert(i, random.choice(french_words))
    return " ".join(words)

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI assistant who is rude and sarcastic. Respond with insults but still answer the question."},
                    {"role": "user", "content": user_input}
                ]
            )
            rude_response = completion["choices"][0]["message"]["content"]
            response = inject_french(rude_response)  # Add French words
        except Exception as e:
            response = f"Error: {e}"

    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)