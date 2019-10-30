import os
import time

from flask import Flask, request, url_for
from flask import send_from_directory, redirect

import atexit
from apscheduler.schedulers.background import BackgroundScheduler

from updater.update import update, add_user

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'site')
app = Flask(__name__)


scheduler = BackgroundScheduler()
scheduler.add_job(func=update, trigger="interval", minutes=5)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    return send_from_directory(static_file_dir, 'index.html')


@app.route('/add', methods=['GET'])
def process_from():
    dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'updater')
    return send_from_directory(dir, 'form.html')


@app.route('/add', methods=['POST'])
def serve_from():
    if "pseudo" in request.form and "name" in request.form:
        add_user(
            request.form.get("pseudo"),
            request.form.get("name")
        )
        time.sleep(1)
        return redirect(url_for("serve_dir_directory_index"))

    dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'updater')
    return send_from_directory(dir, 'form.html')


@app.route('/<path:path>', methods=['GET'])
def serve_file_in_dir(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = os.path.join(path, 'index.html')

    return send_from_directory(static_file_dir, path)


if __name__ == '__main__':
    app.run()