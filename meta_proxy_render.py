
from flask import Flask, request, make_response
import requests

app = Flask(__name__)

VERIFY_TOKEN = 'innerg-secret'
MAKE_WEBHOOK_URL = 'https://hook.make.com/6a4628bb-e74e-4d8e-b2a5-a67b2cdc0d7c'

@app.route('/', methods=['GET', 'POST'])
def meta_proxy():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            response = make_response(str(challenge), 200)
            response.mimetype = 'text/plain'
            return response
        return 'Forbidden', 403

    if request.method == 'POST':
        # Forward to Make.com webhook
        headers = {'Content-Type': 'application/json'}
        try:
            requests.post(MAKE_WEBHOOK_URL, json=request.json, headers=headers)
        except Exception as e:
            print(f"Error forwarding to Make: {e}")
        return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
