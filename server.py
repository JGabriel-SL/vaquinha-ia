from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from datetime import timedelta

import google.generativeai as genai
import json
import os

# Load environment variables from.env file
load_dotenv()
token = os.getenv('API_TOKEN_GEMINI')
token_jwt = os.getenv('JWT_SECRET_KEY')

user_api = os.getenv('USER_REQUEST_API')
pass_api = os.getenv('PASS_REQUEST_API')


# Configuration properties
genai.configure(api_key=token)

config_properties = {
    "temperature": 1,
    "candidate_count": 1
}

# Initialize Flask application
app = Flask(__name__);

app.config["JWT_SECRET_KEY"] = token_jwt;
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app);

# Initialize the Generative Model with the given configuration
model = genai.GenerativeModel("gemini-1.0-pro", generation_config=config_properties)


# Read the criteria to accept the crowdfunding
def read_criteria():
    try:
        with open('./criteria/criteria.txt', 'r', encoding="utf-8") as file:
            criteria = file.read()
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except IOError:
        print("Erro ao ler o arquivo.")
    return criteria

# This function logs a rejected crowdfunding request to the SQL database for further analysis.
def request_rejected(motive):
    print("POST SQL >> Registrando para analise de 2º Instância.")

# This function request to the SQL database for registration
def request_accepted():
    print("POST SQL >> Registrando analise aprovada")

# Endpoint to get the access token to do other requests in the api
@app.route("/login", methods=['POST'])
def login():
    username = request.json['name']
    password = request.json['password']

    if username == user_api and password == pass_api:  
        access_token = create_access_token(identity=username, fresh=True);
        return jsonify(access_token=access_token); 
    else:
        return jsonify({"message": "Invalid credentials"}), 401
 

# Endpoint to accept or reject the crowdfunding request
@app.route('/validate/crowdfunding', methods=['POST'])
@jwt_required()
def validate():   
    title = request.json['title']

    content = request.json['content']
    cash = request.json['cash']

    question = read_criteria();
    question += ".Titulo :" +  title
    question += ".Conteudo: " + content
    question += ".Valor: " + cash

    response = model.generate_content(question)
    objeto_python = json.loads(response.text)

    if objeto_python.get('VALIDATE', '') == '':
        return jsonify({"Error": "Invalid parameter VALIDATE"})
    elif objeto_python.get('MOTIVE', '') == '':
        if (objeto_python.get('VALIDATE')) == 'N':
            return jsonify({"Error": "Invalid parameter MOTIVE"})

    if (objeto_python['VALIDATE'] == 'N'):
            request_rejected(objeto_python['MOTIVE'])
    elif objeto_python['VALIDATE'] == 'S':
        request_accepted()

    return objeto_python

# Start the Flask server
if __name__ == "__main__":
    app.run(debug=True)