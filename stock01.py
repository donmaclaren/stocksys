from flask import Flask, Response, render_template, request,g
import json
from wtforms import TextField,Form,SubmitField
import sqlite3
import string
from forms import AddPart,SearchForm

app = Flask(__name__)

DATABASE = 'stockman.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()






@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    cur = get_db().cursor()  
    pnums = cur.execute("SELECT DESCRIPTION FROM `parts`;").fetchall()
    print(pnums)
    COLUMN = 0
    parts = []
    for prt in pnums:
      if type(prt[COLUMN]) is str:
        parts.append(prt[COLUMN])
    return Response(json.dumps(parts), mimetype='application/json')


@app.route('/parts', methods=['GET', 'POST'])
def parts():
    form = SearchForm(request.form)
    if request.method == "POST":
        dat = form.autocomp.data
        print(dat)
        cur = get_db().cursor()
        res = cur.execute(f"SELECT * FROM `parts` WHERE DESCRIPTION = '{dat}';").fetchone()         
#        print(res)
        return render_template("prt_show.html", res=res[1:], form=form)
    return render_template("prt_search.html", form=form)

@app.route('/removepart')
def removepart():
    return render_template("prt_remove.html")

    
@app.route('/addpart')
def addpart():
    form = AddPart(request.form)
    return render_template("prt_add.html",form=form)

@app.route('/suppliers')
def suppliers():
    return render_template("suppliers.html")

@app.route('/add_supp')
def add_supp():
    return render_template("add_supp.html")
    
@app.route('/rem_supp')
def rem_supp():
    return render_template("rem_supp.html")

    
@app.route('/boms')
def boms():
    return render_template("boms.html")

@app.route('/add_bom')
def add_bom():
    return render_template("add_bom.html")
    
@app.route('/rem_bom')
def rem_bom():
    return render_template("rem_bom.html")
    
@app.route('/')
def index():
    return render_template("main.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False )
