from flask import Flask, render_template, request
import time
import threading
import pyautogui

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


def send_whatsapp_messages(group_ids, message):
    threads = []

    for group_id in group_ids:
        thread = threading.Thread(
            target=send_whatsapp_message, args=(group_id, message))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def send_whatsapp_message(group_id, message):
    try:
        open_group_chat(group_id)
        time.sleep(10)
        pyautogui.typewrite(message)
        pyautogui.press('enter')
    except Exception as e:
        print(
            f"An exception occurred while sending a message to group {group_id}: {str(e)}")


def open_group_chat(group_id):
    group_url = f'https://web.whatsapp.com/accept?code={group_id}'
    pyautogui.hotkey('ctrl', 't')
    pyautogui.typewrite(group_url + '\n')


if __name__ == '__main__':
    app.run()
