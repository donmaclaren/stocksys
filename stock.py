from flask import Flask, Response, render_template, request,g
import json
from wtforms import TextField,Form,SubmitField
import sqlite3

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



class SearchForm(Form):
    autocomp = TextField('Select Part No', id='parts_autocomplete')
    submit = SubmitField('Select')



@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    cur = get_db().cursor()  
    pnums = cur.execute("SELECT PART_NO FROM `parts`;").fetchall()
    print(pnums)
    COLUMN = 0
    parts=[prt[COLUMN] for prt in pnums]
    return Response(json.dumps(parts), mimetype='application/json')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    if request.method == "POST":
        dat = form.autocomp.data
        print(dat)
        cur = get_db().cursor()
        res = cur.execute(f"SELECT * FROM `parts` WHERE PART_NO = '{dat}';").fetchone()         
#        print(res)
        return render_template("parts01.html", res=res[1:], form=form)
    return render_template("search.html", form=form)        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False )
