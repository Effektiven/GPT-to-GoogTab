from flask import Flask, request, jsonify
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests
import os
import json

app = Flask(__name__)

# Читаем ключ из переменной окружения
SERVICE_ACCOUNT_INFO = json.loads(os.environ['GOOGLE_CREDENTIALS'])
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES
)

def get_access_token():
    credentials.refresh(Request())
    return credentials.token

@app.route('/read', methods=['GET'])
def read_sheet():
    spreadsheet_id = request.args.get('spreadsheetId')
    range_ = request.args.get('range')

    token = get_access_token()
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_}'

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)

    return jsonify(response.json()), response.status_code

@app.route('/append', methods=['POST'])
def append_sheet():
    data = request.json
    spreadsheet_id = data['spreadsheetId']
    range_ = data['range']
    values = data['values']

    token = get_access_token()
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_}:append'
    params = {
        'valueInputOption': 'RAW',
        'insertDataOption': 'INSERT_ROWS'
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, params=params, json={'values': values})
    return jsonify(response.json()), response.status_code

@app.route('/update', methods=['PUT'])
def update_sheet():
    data = request.json
    spreadsheet_id = data['spreadsheetId']
    range_ = data['range']
    values = data['values']

    token = get_access_token()
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_}'
    params = {
        'valueInputOption': 'RAW'
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.put(url, headers=headers, params=params, json={'values': values})
    return jsonify(response.json()), response.status_code

@app.route('/clear', methods=['POST'])
def clear_sheet():
    data = request.json
    spreadsheet_id = data['spreadsheetId']
    range_ = data['range']

    token = get_access_token()
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_}:clear'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers)
    return jsonify(response.json()), response.status_code
    
@app.route('/')
def index():
    return 'OK', 200
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
