import flask
from flask import request
import os
from bot import ObjectDetectionBot

app = flask.Flask(__name__)


# TODO load TELEGRAM_TOKEN value from Secret Manager
def get_telegram_token():
    # Specify the secret name
    secret_name = "EDEN-Poly"

    # Create a Secrets Manager client
    client = boto3.client('secretsmanager')

    # Retrieve the secret value
    response = client.get_secret_value(SecretId=secret_name)

    # Parse and return the Telegram token
    secret_string = response['SecretString']
    secret_dict = json.loads(secret_string)
    return secret_dict['TELEGRAM_TOKEN']

if __name__ == "__main__":
    TELEGRAM_TOKEN = get_telegram_token()
    print(f"Telegram Token: {TELEGRAM_TOKEN}")

TELEGRAM_APP_URL = os.environ['TELEGRAM_APP_URL']


@app.route('/', methods=['GET'])
def index():
    return 'Ok'


@app.route(f'/{TELEGRAM_TOKEN}/', methods=['POST'])
def webhook():
    req = request.get_json()
    bot.handle_message(req['message'])
    return 'Ok'


@app.route(f'/results/', methods=['GET'])
def results():
    prediction_id = request.args.get('predictionId')

    # TODO use the prediction_id to retrieve results from DynamoDB and send to the end-user

    chat_id = ...
    text_results = ...

    bot.send_text(chat_id, text_results)
    return 'Ok'


@app.route(f'/loadTest/', methods=['POST'])
def load_test():
    req = request.get_json()
    bot.handle_message(req['message'])
    return 'Ok'


if __name__ == "__main__":
    bot = ObjectDetectionBot(TELEGRAM_TOKEN, TELEGRAM_APP_URL)

    app.run(host='0.0.0.0', port=8443)
