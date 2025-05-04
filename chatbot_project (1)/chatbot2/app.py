from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)
chat_history = []

# Здесь твой API-ключ от OpenRouter
api_key = "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"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.get_json()["message"]
    chat_history.append({"role": "user", "content": user_input})

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": chat_history
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})
    else:
        return jsonify({"reply": "Ошибка связи с OpenRouter, попробуйте позже."})

if __name__ == "__main__":
    app.run(debug=True)
