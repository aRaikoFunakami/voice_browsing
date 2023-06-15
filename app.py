from flask import Flask, render_template, request
import json
import openai_chat
import selenium_browsing
import logging

# フリー素材: https://icooon-mono.com/
app = Flask(__name__, static_folder='./templates', static_url_path='')

# chatgptで作成したseleniumでChromeを操作するコマンド
selenium_command = None

@app.route('/exec', methods=["GET"])
def exec_command():
    global selenium_command
    action=request.args['action']
    if "OK" in action:
        selenium_browsing.exec_command(selenium_command)
    selenium_command = None
    return f"exec_command()" 

@app.route('/input', methods=["GET"])
def input():
    input=request.args['text']
    global selenium_command
    response = openai_chat.generate_selenum_command_by_gpt(input)
    selenium_command = response['command']
    description = response['description']
    logging.info(f"command: {selenium_command}\ndescription: {description}")
    response = { "response": selenium_command, "description": description }
    return json.dumps(response)

@app.route('/')
def index():
    driver = selenium_browsing.get_driver()
    driver.set_window_size(720, 1280)
    return render_template('index.html')

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s:%(name)s - %(message)s")    
app.run(port=8001, debug=True)
