from flask import Flask, render_template, request, jsonify
import requests
import base64

app = Flask(__name__)

# ✅ Replace with your Hugging Face token
HUGGINGFACE_API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/draw", methods=["POST"])
def draw():
    user_input = request.json.get("command", "")
    if not user_input:
        return jsonify({"status": "error", "message": "No voice command received"})

    # 🔍 Analyze user_input to detect style prefix
    if "pencil sketch of" in user_input.lower():
        subject = user_input.lower().replace("pencil sketch of", "").strip()
        prompt = f"high detail pencil sketch drawing of {subject}"
    elif "color drawing of" in user_input.lower():
        subject = user_input.lower().replace("color drawing of", "").strip()
        prompt = f"colored digital art of {subject}, vibrant colors, sharp focus"
    elif "oil painting of" in user_input.lower():
        subject = user_input.lower().replace("oil painting of", "").strip()
        prompt = f"oil painting of {subject}, rich texture, renaissance style"
    else:
        # fallback
        prompt = f"detailed sketch of {user_input}"

    try:
        # 🔁 Send prompt to Hugging Face model
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, stream=True)

        if response.status_code != 200:
            return jsonify({
                "status": "error",
                "message": f"Error {response.status_code}: {response.text}"
            })

        # 📷 Convert image response to base64
        image_data = response.content
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        return jsonify({
            "status": "ok",
            "image": f"data:image/png;base64,{image_base64}"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Exception: {str(e)}"
        })

if __name__ == "__main__":
    app.run(debug=True)
