from flask import Flask, request

from dialog_processor import DialogProcessor
from input_action_type import InputActionType, INPUT_ACTION_NAME_TYPE_MAPPER

app = Flask(__name__)

dialog_processor: DialogProcessor = DialogProcessor()


@app.route('/')  # this is the home page route
def hello_world():  # this is the home page function that generates the page code
    return "Hello world!"


@app.route('/dialog', methods=['POST'])
def dialog():
    req = request.get_json(silent=True, force=True)
    query_result = req.get('queryResult')
    action = query_result.get('action')

    response_text: str = ""
    if action in INPUT_ACTION_NAME_TYPE_MAPPER:
        input_action_type: InputActionType = INPUT_ACTION_NAME_TYPE_MAPPER[action]

        response_text = dialog_processor.process(input_action_type, query_result)

    return {
        "fulfillmentText": response_text,
        "displayText": '25',
        "source": "webhookdata"
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # This line is required to run Flask on repl.it
