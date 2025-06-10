from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/generar-imagen', methods=['POST'])
def generar_imagen():
    data = request.get_json()
    prompt = data.get('prompt')

    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return jsonify({"url": image_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
