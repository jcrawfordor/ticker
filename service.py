from flask import Flask, render_template, request
from escpos.printer import Serial
from data import List, Item, db
import datetime

app = Flask(__name__)
db.connect()
db.create_tables([List, Item])


def build_index(flash=None):
    lists = List.select()
    return render_template('index.html', lists=lists, flash=flash)


def print_list(list):
    p = Serial(devfile="/dev/ttyUSB0", baudrate=38400, bytesize=8, parity='N', stopbits=1, timeout=1.00, dsrdtr=True)
    p.set('center', 'B', 'B', 2, 2)
    p.text(f"{list.name}\n")
    p.set('left', 'A', 'normal', 1, 1)
    for item in list.items:
        p.text(f"[  ] {item.name}\n")
    p.textln()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    p.text(f"as of {date}\n")
    p.cut()


@app.route('/')
def default_ui():
    return build_index()


@app.route('/moditem', methods=['POST'])
def mod_item():
    list_name = request.form['list']
    item_name = request.form['item']
    action = request.form['action']
    if action == "add":
        list = List.select().where(List.name == list_name)

        item_check = Item.select().where(Item.name == item_name, Item.list == list)
        if item_check.exists():
            flash = "Item already exists."
            return build_index(flash)

        item = Item()
        item.name = item_name
        item.list = list
        item.save()
        flash = "Added item"
    if action == "del":
        item = Item.select().where(Item.name == item_name)
        item.delete()
        flash = "Deleted item"
    return build_index(flash)


@app.route('/modlist', methods=['POST'])
def mod_list():
    list_name = request.form['list']
    action = request.form['action']
    if action == "add":
        list = List()
        list.name = list_name
        list.save()
        flash = "List added"
    if action == "del":
        list = List.select().where(List.name == list_name)
        list.delete()
        flash = "List deleted"
    if action == "print":
        list = List.select().where(List.name == list_name)
        print_list(list)
    return build_index(flash)
