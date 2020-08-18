from flask import Flask, Response, render_template, request,g
import json
from wtforms import TextField,Form,SubmitField
import sqlite3
import string
from forms import AddPart,SearchForm, BomForm
import io
import csv

app = Flask(__name__)

DATABASE = 'stockman.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def add_part(data):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO `parts` (PART_NO, DESCRIPTION, SUPPLIER, ORDER_CODE, COST_PRICE, DELIVERED_PRICE, STOCK,\
                UNIT, LEADTIME, LOCATION, REORDER_QTY, OWNER, SUPPLIER2, ORDER_CODE2) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",data)
    conn.commit()
    return cur.lastrowid
    
def delete_part(part):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM 'parts' WHERE PART_NO = '{part}'")
    conn.commit()
#    return cur.lastrowid

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/autocomplete_supp', methods=['GET'])
def autocomplete_supp():
    cur = get_db().cursor()  
    pnums = cur.execute("SELECT COMPANY FROM `companys`;").fetchall()
    print(pnums)
    COLUMN = 0
    parts = []
    for prt in pnums:
      if type(prt[COLUMN]) is str:
        parts.append(prt[COLUMN])
    return Response(json.dumps(parts), mimetype='application/json')

@app.route('/autocomplete_bom', methods=['GET'])
def autocomplete_bom():
    cur = get_db().cursor()  
    desc = cur.execute("SELECT DESCRIPTION FROM `bom_headers`;").fetchall()
#    print(desc)
    COLUMN = 0
    boms = []
    for ds in desc:
      if type(ds[COLUMN]) is str:
        boms.append(ds[COLUMN])
    return Response(json.dumps(boms), mimetype='application/json')

@app.route('/autocomplete_part', methods=['GET'])
def autocomplete_part():
    cur = get_db().cursor()  
    pnums = cur.execute("SELECT PART_NO FROM `parts`;").fetchall()
    print(pnums)
    COLUMN = 0
    parts = []
    for prt in pnums:
      if type(prt[COLUMN]) is str:
        parts.append(prt[COLUMN])
    return Response(json.dumps(parts), mimetype='application/json')
    
@app.route('/autocomplete_desc', methods=['GET'])
def autocomplete_desc():
    cur = get_db().cursor()  
    pnums = cur.execute("SELECT DESCRIPTION FROM `parts`;").fetchall()
    print(pnums)
    COLUMN = 0
    parts = []
    for prt in pnums:
      if type(prt[COLUMN]) is str:
        parts.append(prt[COLUMN])
    return Response(json.dumps(parts), mimetype='application/json')
    
@app.route('/autocomplete_code', methods=['GET'])
def autocomplete_code():
    cur = get_db().cursor()  
    pnums = cur.execute("SELECT ORDER_CODE FROM `parts`;").fetchall()
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
        dat1 = form.autocomp1.data
        print(dat1)
        dat2 = form.autocomp2.data
        print(dat2)
        cur = get_db().cursor()
        if len(dat) > 2:
          res = cur.execute(f"SELECT * FROM `parts` WHERE PART_NO = '{dat}';").fetchone() 
        elif len(dat1) > 2:
          res = cur.execute(f"SELECT * FROM `parts` WHERE DESCRIPTION = '{dat1}';").fetchone()
        elif len(dat2) > 2:
          res = cur.execute(f"SELECT * FROM `parts` WHERE ORDER_CODE = '{dat2}';").fetchone()
#        print(res)
        form = AddPart()
#        form.part_no.data = res[1]
        i = 1
        for field in form:
            if 'supplier' in field.name  and len(res[i]) != 0:
                 dat = res[i]
                 field.data = cur.execute(f"SELECT COMPANY FROM `companys` WHERE COMP_NO = '{dat}';").fetchone()[0]
            else:
                 field.data = res[i]
            i += 1
        return render_template("prt_show.html", res=res[1:], form=form)
    return render_template("prt_search.html", form=form)

# Save an edited part
@app.route('/savepart', methods=['GET', 'POST'])
def savepart():
    form = AddPart(request.form)
    if request.method == "POST":    
#        dat = form.part_no.data
#        delete_part(dat)
        return("SAVED!")
    return render_template("prt_remove.html",form=form)


# Remove a part from db
@app.route('/removepart', methods=['GET', 'POST'])
def removepart():
    form = AddPart(request.form)
    if request.method == "POST":    
        dat = form.part_no.data
        delete_part(dat)
        return render_template("prt_removed.html")
    return render_template("prt_remove.html",form=form)

# Add a new part    
@app.route('/addpart', methods=['GET', 'POST'])
def addpart():
    form = AddPart(request.form)
    if request.method == "POST":
        cur = get_db().cursor()
        dat = []
        for field in form:
          if 'supplier' in field.name  and len(field.data) != 0:
            field.data = cur.execute(f"SELECT COMP_NO FROM `companys` WHERE COMPANY = '{field.data}';").fetchone()[0]
          dat.append(field.data)
        print(dat)
        add_part(dat)
#        cur = get_db().cursor()
#        res = cur.execute(f"SELECT * FROM `parts` WHERE PART_NO = '{dat}';").fetchone()
        return render_template("prt_saved.html")
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

    
@app.route('/boms', methods=['GET', 'POST'])
def boms():
    form = BomForm(request.form)
    if request.method == "POST":
        dat = form.autocomp_bom.data
        print(dat)
        qty = form.qty_bom.data
        print(qty)

        cur = get_db().cursor()
        if len(dat) > 2:
          bom = cur.execute(f"SELECT * FROM `bom_headers` WHERE DESCRIPTION = '{dat}';").fetchone()
          print(bom)
          
          bom_no = bom[0] 

          try:
              cur.execute(f"SELECT PART_NO, DESCRIPTION, QTY_USED, CCTLOC FROM `bom_items` WHERE BOM = '{bom_no}';")
              result = cur.fetchall()
              print(result)
      
              output = io.StringIO()
              writer = csv.writer(output, quoting=csv.QUOTE_NONE, escapechar=' ')

              line = [bom[1] + ',' + bom[2]]
              writer.writerow(line)
          
              line = ['PART NO, DESCRIPTION, QTY REQ, QTY STOCK, TO ORDER, CCT Loc']
              writer.writerow(line)
      
      
              for row in result:
                  req = float(row[2])*int(qty)
                  req = round(req,2)
                  part = cur.execute(f"SELECT * FROM `parts` WHERE PART_NO = '{row[0]}';").fetchone()
                  print(part)
                  stock = float(part[7])
                  stock = round(stock,2)
                  if stock < req:
                    order = req - stock
                  else:
                    order = 0
                  order = round(order,2)
                  line = [ row[0] + ',' + row[1].replace(',',' ') + ',' + str(req) + ',' + str(stock) + ',' + str(order) + ',' + row[3].replace(',',' ')]
                  writer.writerow(line)
      
              output.seek(0)
          
              return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=bom_report.csv"})
          except Exception as e:
              print(e)
          finally:
              pass   
    
    
    
    return render_template("boms.html",form=form)

@app.route('/add_bom')
def add_bom():
    return render_template("add_bom.html")
    
@app.route('/rem_bom')
def rem_bom():
    return render_template("rem_bom.html")
    
@app.route('/')
def index():
    return render_template("main.html")
    
@app.route('/download/report/csv')
def download_report():
    try:
#		conn = mysql.connect()
#		cursor = conn.cursor(pymysql.cursors.DictCursor)
        cur = get_db().cursor()
		
        cur.execute("SELECT BOM, PART_NO, DESCRIPTION, QTY_USED, CCTLOC FROM `bom_items` WHERE BOM = 402;")
        result = cur.fetchall()
        print(result)

        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_NONE, escapechar=' ')
#        writer = csv.writer(output)
		
        line = ['BOM, PART_NO, DESCRIPTION, QTY_USED, CCT Loc']
        writer.writerow(line)


        for row in result:
            line = [str(row[0]) + ',' + row[1] + ',' + row[2].replace(',',' ') + ',' + row[3]+ ',' + row[4].replace(',',' ')]
#            line = [str(row['BOM']) + ',' + row['PART_NO'] + ',' +'"' + row['DESCRIPTION'] +'"' + ',' + row['QTY_USED']+ ',' + row['CCTLOC']]
            writer.writerow(line)

        output.seek(0)
		
        return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=bom_report.csv"})
    except Exception as e:
        print(e)
    finally:
#		cursor.close() 
#		conn.close()
        pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True, use_reloader=False )
