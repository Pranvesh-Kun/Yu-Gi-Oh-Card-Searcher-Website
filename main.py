from requests import request as req
from flask import Flask, render_template, request
import urllib.request
import os


def download_image(image_url, file_dir):
    directory = os.path.dirname(file_dir)
    if not os.path.exists(directory):
        os.makedirs(directory)
    urllib.request.urlretrieve(image_url, file_dir)


app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def home():
    return render_template("index.html")


@app.route('/search', methods=["POST", "GET"])
def search():
    extra = False
    non_monster = False
    if request.method == "POST":
        response = req(url=f"https://db.ygoprodeck.com/api/v7/cardinfo.php?name={request.form.get('input')}", method="GET")
        data = response.json()
        if response.status_code == 200:
            if '\n' in data['data'][0]['desc']:
                data['data'][0]['desc1'] = data['data'][0]['desc'].split("\n")[0]
                data['data'][0]['desc2'] = data['data'][0]['desc'].split("\n")[1]
                extra = True
            if data['data'][0]['type'] == "Spell Card" or data['data'][0]['type'] == "Trap Card":
                non_monster = True
            download_image(data['data'][0]['card_images'][0]['image_url_small'], f"C:/Users/VBALAJI/PycharmProjects/Custom Website/static/img/{data['data'][0]['id']}.jpg")
            return render_template('index.html', card=data, extra=extra, nomon=non_monster)
        else:
            return render_template("index.html", card=False, extra=extra, nomon=non_monster)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
