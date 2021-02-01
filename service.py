from flask import Flask, render_template, request
from escpos.printer import Serial
from data import List, Item, db
from datetime import datetime

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
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    p.set('right', 'B', 'normal', 1, 1)
    p.text(f"\nas of {date}\n")
    p.cut()


@app.route('/', methods=['GET', 'POST'])
def default_ui():
    if 'object' in request.form:
        if request.form['object'] == "item":
            return mod_item(request)
        elif request.form['object'] == "list":
            return mod_list(request)
    else:
        return build_index()


def mod_item(request):
    list_name = request.form['list']
    item_name = request.form['item']
    action = request.form['action']
    if action == "add":
        list = List.get(List.name == list_name)
        item = Item.get_or_create(name=item_name, list=list)
        flash = "Added item"
    if action == "del":
        list = List.get(List.name == list_name)
        item = Item.get(Item.name == item_name, Item.list == list)
        item.delete_instance()
        flash = "Deleted item"
    return build_index(flash)


def mod_list(request):
    list_name = request.form['list']
    action = request.form['action']
    if action == "add":
        list = List.get_or_create(name=list_name)
        flash = "List added"
    if action == "delete":
        if 'confirm' in request.form and request.form['confirm'] == 'true':
            list = List.get(List.name == list_name)
            list.delete_instance()
            flash = "List deleted"
        else:
            return render_template('confirm.html', action=action, list=list)
    if action == "clear":
        if 'confirm' in request.form and request.form['confirm'] == 'true':
            list = List.get(List.name == list_name)
            query = Item.delete().where(Item.list == list).execute()
            flash = "List cleared"
        else:
            return render_template('confirm.html', action=action, list=list)
    if action == "print":
        list = List.get(List.name == list_name)
        print_list(list)
        flash = "Printed list"
    if action == "cancel":
        flash = "Cancelled"
    return build_index(flash)
