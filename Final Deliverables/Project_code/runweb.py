import email
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
import os
import ibm_db
import re
import datetime


app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'lackhmi.priya2001_ec@mepcoeng.ac.in'
app.config['MAIL_PASSWORD'] = 'priya2112!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.secret_key = 'a'
conn = ibm_db.connect('DATABASE=bludb;HOSTNAME=54a2f15b-5c0f-46df-8954-7e38e612c2bd.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32733;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=pym84828;PWD=dO5pMDCTkL3mSV58', '', '')

global cost


@app.route('/', methods=['GET', 'POST'])
def register():
    msg = " "
    if request.method == 'POST':
        username = request.form.get('user')
        email = request.form.get('email')
        password = request.form.get('password')
        sql = 'select * from user where username=?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = "account already exists!"
            return redirect(url_for('login'))
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = "invalid email address"
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers'
        else:
            insert_sql = 'insert into user values(?,?,?)'
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)
            #msg='you have succesfully logged in'
            msg = 'please fill out of the form'
            return redirect(url_for('login'))
    return render_template('login.html', msg=msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global userid
    msg = ""
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('password')
        sql = "select * from user where username=? and password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin'] = True
            session['id'] = account['USERNAME']
            userid = account["USERNAME"]
            session['username'] = account['USERNAME']
            msg = 'logged in succesfully'
            return redirect(url_for('dashboard'))
        else:
            msg = 'incorrect username password'
    return render_template('login.html', msg=msg)


@app.route('/mail', methods=['POST'])
def mailfunc():
    if request.form.get('mail') == 'Send Mail':
        msg = Message("hi", sender='lackhmi.priya2001_ec@mepcoeng.ac.in',
                      recipients=['lkpriya200107@gmail.com'])
        msg.body = "Unavailable Stock"
        mail.send(msg)
        return "Sent Mail"
    return render_template('sales.html')


@app.route('/sup', methods=['POST'])
def sup():
    global userid
    data = ""
    if request.form.get('run1') == 'Add':
        ivno = request.form.get('ivno')
        emai = request.form.get('emai')
        nam = request.form.get('nam')
        con = request.form.get('con')
        qt = request.form.get('qt')
        insert_sql = 'insert into supplier values(?,?,?,?,?)'
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, ivno)
        ibm_db.bind_param(prep_stmt, 2, emai)
        ibm_db.bind_param(prep_stmt, 3, nam)
        ibm_db.bind_param(prep_stmt, 4, con)
        ibm_db.bind_param(prep_stmt, 5, qt)
        ibm_db.execute(prep_stmt)
        return redirect(url_for('supply'))
    if request.form.get("run4") == "Show":
        return redirect(url_for('getsup'))
    if request.form.get("run3") == "Delete":
        return redirect(url_for('delsup'))
    return render_template('supplier.html')


@app.route('/delup', methods=['POST'])
def delup():
    print('yes')
    if request.form.get("delinvoice") == "Delete":
        print('yes')
        inv = request.form.get('invoice')
        del_sql = 'delete from SUPPLIER where INVOICE_NUMBER=?'
        prep_stmt = ibm_db.prepare(conn, del_sql)
        ibm_db.bind_param(prep_stmt, 1, inv)
        print('prep_stmt')
        ibm_db.execute(prep_stmt)
        return redirect(url_for('getsup'))
    return render_template('delup.html')


def method_name():
    pass


@app.route('/addCust', methods=['POST'])
def addCust():
    global userid
    data = ""
    if request.form.get("action1") == "Add":
        empid = request.form.get('empid')
        username = request.form.get('user')
        email = request.form.get('email')
        password = request.form.get('pass')
        insert_sql = 'insert into employe values(?,?,?,?)'
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, empid)
        ibm_db.bind_param(prep_stmt, 2, username)
        ibm_db.bind_param(prep_stmt, 3, email)
        ibm_db.bind_param(prep_stmt, 4, password)
        ibm_db.execute(prep_stmt)
        return redirect(url_for('employee'))
    if request.form.get("sho") == "Show":
        return redirect(url_for('getCust'))
    if request.form.get("ac3") == "Delete":
        return redirect(url_for('dell'))
    return render_template('employee_details.html')


@app.route('/delcus', methods=['POST'])
def delcus():
    global userid
    data = ""
    if request.form.get("del") == "Delete":
        empid = request.form.get('empid')
        del_sql = 'delete from EMPLOYE where EMP_ID=?'
        prep_stmt = ibm_db.prepare(conn, del_sql)
        ibm_db.bind_param(prep_stmt, 1, empid)
        ibm_db.execute(prep_stmt)
        return redirect(url_for('getCust'))
    return render_template('delcust.html')


@app.route('/dispcust.html', methods=['GET'])
def getCust():
    global userid
    dat = []
    id = []
    name = []
    email = []
    pwrd = []
    sql = "select * from EMPLOYE"
    stmt = ibm_db.prepare(conn, sql)
    stmt = ibm_db.exec_immediate(conn, sql)
    account = ibm_db.fetch_assoc(stmt)
    while account != False:
        id.append(account["EMP_ID"])
        name.append(account["NAME"])
        email.append(account["EMAIL"])
        pwrd.append(account["PASSWORD"])
        account = ibm_db.fetch_assoc(stmt)

    return render_template('dispcust.html', data=zip(id, name, email, pwrd))


@app.route('/dispsup.html', methods=['GET'])
def getsup():
    global userid
    qty = []
    invo = []
    email = []
    supname = []
    conc = []
    sql = "select * from SUPPLIER"
    stmt = ibm_db.prepare(conn, sql)
    stmt = ibm_db.exec_immediate(conn, sql)
    account = ibm_db.fetch_assoc(stmt)
    while account != False:
        invo.append(account["INVOICE_NUMBER"])
        email.append(account["EMAIL"])
        supname.append(account["SUPPLIER_NAME"])
        conc.append(account["CONTACT_NUMBER"])
        qty.append(account["QUANTITY"])
        account = ibm_db.fetch_assoc(stmt)
    return render_template('dispsup.html', data=zip(invo, email, supname, conc, qty))


@app.route('/dispproduct.html', methods=['GET'])
def getproduct():
    global userid
    cat = []
    sup = []
    proname = []
    proprice = []
    qty = []
    sql = "select * from PRODUCT"
    stmt = ibm_db.prepare(conn, sql)
    stmt = ibm_db.exec_immediate(conn, sql)
    account = ibm_db.fetch_assoc(stmt)
    while account != False:
        cat.append(account["CATEGORY"])
        sup.append(account["SUPPLIER_NAME"])
        proname.append(account["PRODUCT_NAME"])
        proprice.append(account["PRODUCT_PRICE"])
        qty.append(account["QUANTITY"])
        account = ibm_db.fetch_assoc(stmt)
    return render_template('dispproduct.html', data=zip(cat, sup, proname, proprice, qty))


@app.route('/dispcat.html', methods=['GET'])
def getcat():
    global userid
    cat = []
    sql = "select * from CATEGORY"
    stmt = ibm_db.prepare(conn, sql)
    stmt = ibm_db.exec_immediate(conn, sql)
    account = ibm_db.fetch_assoc(stmt)
    while account != False:
        cat.append(account["CATEGORIES"])
        account = ibm_db.fetch_assoc(stmt)
    return render_template('dispcat.html', data=cat)


@app.route('/category', methods=['POST'])
def categorydef():
    global userid
    data = ""
    if request.form.get('cat1') == 'Add':
        cat = request.form.get('cat')
        insert_sql = 'insert into category values(?)'
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, cat)
        ibm_db.execute(prep_stmt)
        return redirect(url_for('category'))
    if request.form.get('cat3') == 'Show':
        return redirect(url_for('getcat'))
    if request.form.get('cat2') == 'Delete':
        cat1 = request.form.get('cat')
        del_sql = 'delete from category where categories=?'
        prep_stmt1 = ibm_db.prepare(conn, del_sql)
        ibm_db.bind_param(prep_stmt1, 1, cat1)
        ibm_db.execute(prep_stmt1)
    return render_template('categories.html')


@app.route('/product', methods=['GET', 'POST'])
def product():
    global userid
    if request.form.get('do1') == 'Add':
        catchoose = request.form.get('drop1')
        supchoose = request.form.get('drop2')
        nam = request.form.get('nam')
        pri = request.form.get('pri')
        qt = request.form.get('qt')
        insert_sql = 'insert into PRODUCT values(?,?,?,?,?)'
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, catchoose)
        ibm_db.bind_param(prep_stmt, 2, supchoose)
        ibm_db.bind_param(prep_stmt, 3, nam)
        ibm_db.bind_param(prep_stmt, 4, pri)
        ibm_db.bind_param(prep_stmt, 5, qt)
        ibm_db.execute(prep_stmt)
        return redirect(url_for('productfinal'))
    if request.form.get('do4') == 'Show':
        return redirect(url_for('getproduct'))
    if request.form.get('do3') == 'Delete':
        return redirect(url_for('delproduct'))
    return render_template('product.html')
    # print(account)
    # s=[]
    # for x in account.values():
    #    print(x)
    #   s.append(x)
    #   print(s)


@app.route('/delprod', methods=['POST'])
def delprod():
   # global userid
   # s1 = []
   # print("inside")
    #sql1 = "select PRODUCT_NAME from PRODUCT"
    #stmt1 = ibm_db.exec_immediate(conn, sql1)
    #account1 = ibm_db.fetch_assoc(stmt1)
    # print(account1)
    # while account1 != False:
    #   s1.append(account1["PRODUCT_NAME"])
    #  account1 = ibm_db.fetch_assoc(stmt1)
    # print(s1)
    if request.form.get("delinvoice") == "Delete":
        prodname = request.form.get('prod_name')
        del_sql = 'delete from PRODUCT where PRODUCT_NAME=?'
        prep_stmt = ibm_db.prepare(conn, del_sql)
        ibm_db.bind_param(prep_stmt, 1, prodname)
        ibm_db.execute(prep_stmt)
        return redirect(url_for('getproduct'))
    return render_template('delprod.html')


@app.route('/dashboardfinal.html')
def dashboard():
    sql = "select count(*) from employe"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    for x in account.values():
        s = x
    sql1 = "select count(*) from supplier"
    stmt1 = ibm_db.prepare(conn, sql1)
    ibm_db.execute(stmt1)
    account1 = ibm_db.fetch_assoc(stmt1)
    for x1 in account1.values():
        s1 = x1
    sql2 = "select count(*) from category"
    stmt2 = ibm_db.prepare(conn, sql2)
    ibm_db.execute(stmt2)
    account2 = ibm_db.fetch_assoc(stmt2)
    for x2 in account2.values():
        s2 = x2
    sql3 = "select count(*) from product"
    stmt3 = ibm_db.prepare(conn, sql3)
    ibm_db.execute(stmt3)
    account3 = ibm_db.fetch_assoc(stmt3)
    for x3 in account3.values():
        s3 = x3
    return render_template("dashboardfinal.html", ye=s1, yes=s, cate=s2, pro=s3)


@app.route('/addcart', methods=['POST'])
def addcart():
    global userid
    data = ""
    if request.form.get("action9") == "Add to cart":
        p_name = request.form.get('object1')
        p_price = request.form.get('object2')
        quant = request.form.get('object3')
        insert_sql = 'insert into ADDCART values(?,?,?)'
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, p_name)
        ibm_db.bind_param(prep_stmt, 2, p_price)
        ibm_db.bind_param(prep_stmt, 3, quant)
        ibm_db.execute(prep_stmt)
        return render_template('orders.html')
    if request.form.get("action8") == "Show":
        return redirect(url_for('getCart'))
    return render_template('orders.html')


@app.route('/addtoCart.html', methods=['GET', 'POST'])
def getCart():
    global userid
    p_n = []
    p_p = []
    qua = []
    tot = []
    dash = {}
    sql = "select * from ADDCART"
    stmt = ibm_db.prepare(conn, sql)
    stmt = ibm_db.exec_immediate(conn, sql)
    account = ibm_db.fetch_assoc(stmt)
    while account != False:
        dash[account["PRODUCT_NAME"]] = account["QUANTITY"]
        p_n.append(account["PRODUCT_NAME"])
        p_p.append(account["PRICE"])
        qua.append(account["QUANTITY"])
        tot.append(account["PRICE"]*account["QUANTITY"])
        account = ibm_db.fetch_assoc(stmt)
    cost = sum(tot)
    if request.form.get("buy") == "BUY_NOW":
        return redirect(url_for('buyth'))
    return render_template('addtocart.html', data=zip(p_n, p_p, qua, tot), cost=cost)


@app.route('/buynow', methods=['POST', 'GET'])
def buynow():
    salesprod = {}
    print("inside")
    sqlstmt = "select * from ADDCART"
    stmtex = ibm_db.prepare(conn, sqlstmt)
    stmtex = ibm_db.exec_immediate(conn, sqlstmt)
    accountf = ibm_db.fetch_assoc(stmtex)
    while accountf != False:
        salesprod[accountf["PRODUCT_NAME"]] = accountf["QUANTITY"]
        accountf = ibm_db.fetch_assoc(stmtex)
    print(salesprod)
    for i, j in salesprod.items():
        insert_sql = 'insert into SALES values(?,?,?)'
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, i)
        ibm_db.bind_param(prep_stmt, 2, j)
        ibm_db.bind_param(prep_stmt, 3, datetime.datetime.now())
        ibm_db.execute(prep_stmt)
    dash = {}
    tot = []
    sql = "select * from ADDCART"
    stmt = ibm_db.prepare(conn, sql)
    stmt = ibm_db.exec_immediate(conn, sql)
    account = ibm_db.fetch_assoc(stmt)
    while account != False:
        dash[account["PRODUCT_NAME"]] = account["QUANTITY"]
        tot.append(account["PRICE"]*account["QUANTITY"])
        account = ibm_db.fetch_assoc(stmt)
    cost = sum(tot)
    for i, j in dash.items():
        get1 = "select QUANTITY from PRODUCT where PRODUCT_NAME=?"
        prep_stmt1 = ibm_db.prepare(conn, get1)
        ibm_db.bind_param(prep_stmt1, 1, i)
        stmt1 = ibm_db.execute(prep_stmt1)
        account1 = ibm_db.fetch_assoc(prep_stmt1)
        value1 = account1['QUANTITY']-j
        print(type(account1['QUANTITY']))
        print(type(j))
        print(account1['QUANTITY'])
        print(j)
        print(value1)
        set1 = "update product set QUANTITY=? where PRODUCT_NAME=?"
        prepare1 = ibm_db.prepare(conn, set1)
        ibm_db.bind_param(prepare1, 1, value1)
        ibm_db.bind_param(prepare1, 2, i)
        ibm_db.execute(prepare1)
    del_sql = 'delete from ADDCART'
    del_stmt = ibm_db.prepare(conn, del_sql)
    ibm_db.execute(del_stmt)
    return render_template('buynow.html', msg=cost)


@app.route('/orders.html', methods=['GET'])
def orders():
    global userid
    dat = []
    prod_name = []
    price = []
    sql = "select * from PRODUCT"
    stmt = ibm_db.prepare(conn, sql)
    stmt = ibm_db.exec_immediate(conn, sql)
    account = ibm_db.fetch_assoc(stmt)
    print(account)
    while account != False:
        prod_name.append(account["PRODUCT_NAME"])
        price.append(account["PRODUCT_PRICE"])
        account = ibm_db.fetch_assoc(stmt)

    return render_template('orders.html', data=zip(prod_name, price))


@app.route('/sales.html')
def salesf():
    prod_name = []
    qty = []
    prod_nam = []
    qt = []
    salemail={}
    sql = "select * from SALES order BY SALESDATE DESC  LIMIT 5"
    stmt = ibm_db.prepare(conn, sql)
    stmt = ibm_db.exec_immediate(conn, sql)
    account = ibm_db.fetch_assoc(stmt)
    print(account)

    while account != False:
        prod_name.append(account["PRODUCT_NAME"])
        qty.append(account["QUANTITY"])
        account = ibm_db.fetch_assoc(stmt)

    sql1 = "select * from PRODUCT where QUANTITY < 10"
    stmt1 = ibm_db.prepare(conn, sql1)
    stmt1 = ibm_db.exec_immediate(conn, sql1)
    account1 = ibm_db.fetch_assoc(stmt1)
    print(account1)
    co=0
    while account1 != False:
        co=co+1
        prod_nam.append(account1["PRODUCT_NAME"])
        qt.append(account1["QUANTITY"])
        salemail[account1["PRODUCT_NAME"]]=account1["QUANTITY"]
        account1 = ibm_db.fetch_assoc(stmt1)
    if(co>0):
        msg = Message("Items less in Stock", sender='lackhmi.priya2001_ec@mepcoeng.ac.in',
                      recipients=['lkpriya200107@gmail.com'])
        msg.html= render_template('mailsent.html',salemail=salemail)        
        msg.body = "products less in stock"
        mail.send(msg)
    return render_template('sales.html', data=zip(prod_name, qty), dat=zip(prod_nam, qt), f=prod_name, q=qty)

@app.route('/product.html')
def productfinal():
    data = []
    s = []
    s1 = []
    data1 = []
    sql = "select categories from category"
    stmt = ibm_db.exec_immediate(conn, sql)
    account = ibm_db.fetch_assoc(stmt)
    while account != False:
        s.append(account["CATEGORIES"])
        account = ibm_db.fetch_assoc(stmt)
    sql1 = "select SUPPLIER_NAME from SUPPLIER"
    stmt1 = ibm_db.exec_immediate(conn, sql1)
    account1 = ibm_db.fetch_assoc(stmt1)
    while account1 != False:
        s1.append(account1["SUPPLIER_NAME"])
        account1 = ibm_db.fetch_assoc(stmt1)
    return render_template("/product.html", data=s, data1=s1)

@app.route('/supplier.html')
def supply():
    return render_template("supplier.html")


@app.route('/delprod.html')
def delproduct():
    return render_template("/delprod.html")


@app.route('/employee_details.html')
def employee():
    return render_template("/employee_details.html")


@app.route('/categories.html')
def category():
    return render_template("/categories.html")


@app.route('/login.html')
def signout():
    return render_template("/login.html")


@app.route('/delcust.html')
def dell():
    return render_template("/delcust.html")


@app.route('/delup.html')
def delsup():
    return render_template("/delup.html")


@app.route('/buynow.html')
def buyth():
    return render_template("/buynow.html")
@app.route('/mailsent.html')
def mails():
    return render_template("/mailsent.html")


if __name__ == '__main__':
    app.run(debug=True)
