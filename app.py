from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/generar-cuento', methods=['POST'])
def generar_cuento():
    data = request.get_json()
    nombre = data.get("nombre")
    edad = data.get("edad")
    tema = data.get("tema")

    try:
        prompt = f"Escribe un cuento para colorear para un niño de {edad} años llamado {nombre}, sobre el tema: {tema}. Divide el cuento en 3 páginas con texto breve por página."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        cuento_texto = response.choices[0].message.content

        # Dividir el texto en páginas si es posible
        paginas = [{"texto": parte.strip()} for parte in cuento_texto.split("\n\n") if parte.strip()]

        return jsonify({"paginas": paginas})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
