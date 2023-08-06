from flask import Flask, render_template, request
import time
import pyautogui
import threading
from concurrent.futures  import ThreadPoolExecutor

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        group_ids = request.form['group_id'].split(',')  
        message = request.form['message']

        try:
            send_whatsapp_messages(group_ids, message)  
            return "WhatsApp messages sent successfully."
        except Exception as e:
            return f"An exception occurred while sending the WhatsApp messages: {str(e)}"

    return render_template('index.html')


def send_whatsapp_message(group_ids, message):
    for group_id in group_ids:
        open_group_chat(group_id)
        time.sleep(10) 
        pyautogui.typewrite(message)
        pyautogui.press('enter')
        time.sleep(5)  
def send_whatsapp_messages(group_ids ,message):
    l = []
    l.append(group_ids)
    c = []
    c.append(message)
    with ThreadPoolExecutor(max_workers=2) as executor:
      future = executor.map(send_whatsapp_message,l , c)
      

def open_group_chat(group_id):
    group_url = f'https://web.whatsapp.com/accept?code={group_id}'
    pyautogui.hotkey('ctrl', 't')
    pyautogui.typewrite(group_url + '\n')


if __name__ == '__main__':
    app.run(debug = True)