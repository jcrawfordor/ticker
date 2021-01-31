from flask import Flask, render_template, request
from escpos.printer import Serial
from data import List, Item
import configparser

app = Flask(__name__)

def get_printer():
    return Serial(devfile="/dev/ttyUSB0", baudrate=38400, bytesize=8, parity='N', stopbits=1, timeout=1.00, dsrdtr=True)

@app.route('/')
def default_ui():
    # Get the lists we need to work on
    lists = Lists.select()
    return render_template('index.html', lists=lists)

@app.route('/additem', methods=['POST'])
def add_item():
    if 'item' in request.form:
        item = request.form['item']
        p = get_printer()
        p.text(f"{item}\n")
    return render_template('index.html')
