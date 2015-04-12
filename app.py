from flask import Flask, render_template
from pysnap import Snapchat

app = Flask(__name__)
snap = Snapchat('secondwindsnaps', '2433fd63b5389757d0786ebf056a946e')

@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
    app.run()