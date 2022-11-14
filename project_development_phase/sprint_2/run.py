import email
from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import re
app=Flask(__name__)
app.secret_key='a'
conn=ibm_db.connect('DATABASE=bludb;HOSTNAME=54a2f15b-5c0f-46df-8954-7e38e612c2bd.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32733;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=pym84828;PWD=dO5pMDCTkL3mSV58','','')
@app.route('/',methods=['GET','POST'])
def register():
    msg=" "
    if request.method=='POST':
        username=request.form.get('user')
        email=request.form.get('email')
        password=request.form.get('password')
        sql='select * from user where username=?'
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg="account already exists!"
            return redirect(url_for('login'))
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg="invalid email address"
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg='name must contain only characters and numbers'
        else:
            insert_sql='insert into user values(?,?,?)'
            prep_stmt=ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,username)
            ibm_db.bind_param(prep_stmt,2,email)    
            ibm_db.bind_param(prep_stmt,3,password)
            ibm_db.execute(prep_stmt)
            #msg='you have succesfully logged in'
            msg='please fill out of the form'
            return redirect(url_for('login'))
    return render_template('login.html',msg=msg)
@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg=""
    if request.method=='POST':
        username=request.form.get('user')
        password=request.form.get('password')
        sql="select * from user where username=? and password=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin']=True
            session['id']=account['USERNAME']
            userid=account["USERNAME"]
            session['username']=account['USERNAME']
            msg='logged in succesfully'
            return redirect(url_for('dashboard'))
        else:
            msg='incorrect username password'
    return render_template('login.html',msg=msg)
@app.route('/sup', methods=['POST'])
def sup():
    global userid
    data = ""
    if request.method == 'POST':
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
    return render_template('supplier.html')
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
        return redirect(url_for('addCust'))
    if request.form.get("sho") == "Show":
        return redirect(url_for('getCust'))
    return render_template('employee_details.html') 
@app.route('/dispcust.html', methods=['GET'])
def getCust():
    global userid
    dat=[]
    id=[]
    name=[]
    email=[]
    pwrd=[]
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

    return render_template('dispcust.html',data=zip(id,name,email,pwrd))
@app.route('/category', methods=['POST'])
def categorydef():
    global userid
    data = ""
    if request.method == 'POST':
        cat = request.form.get('cat')
        insert_sql = 'insert into category values(?)'
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, cat)
        ibm_db.execute(prep_stmt)
    return render_template('categories.html')
@app.route('/product', methods=['GET','POST'])
def product():
    global userid
    if request.method == 'POST':
        catchoose = request.form.get('drop1')
        supchoose = request.form.get('drop2')
        nam = request.form.get('nam')
        pri = request.form.get('pri')
        qt = request.form.get('qt')
        insert_sql = 'insert into product values(?,?,?,?,?)'
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, catchoose)
        ibm_db.bind_param(prep_stmt, 2, supchoose)
        ibm_db.bind_param(prep_stmt, 3, nam)
        ibm_db.bind_param(prep_stmt, 4, pri)
        ibm_db.bind_param(prep_stmt, 5, qt)
        ibm_db.execute(prep_stmt)
        return redirect(url_for('productfinal'))
    return render_template('product.html')
    #print(account)
    #s=[]
    #for x in account.values():
    #    print(x)
    #   s.append(x)
    #   print(s)
@app.route('/dashboardfinal.html')
def dashboard():
    sql = "select count(*) from employe"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    for x in account.values():
        s=x
    sql1 = "select count(*) from supplier"
    stmt1 = ibm_db.prepare(conn, sql1)
    ibm_db.execute(stmt1)
    account1 = ibm_db.fetch_assoc(stmt1)
    for x1 in account1.values():
        s1=x1
    sql2 = "select count(*) from category"
    stmt2 = ibm_db.prepare(conn, sql2)
    ibm_db.execute(stmt2)
    account2 = ibm_db.fetch_assoc(stmt2)
    for x2 in account2.values():
        s2=x2
    sql3 = "select count(*) from product"
    stmt3 = ibm_db.prepare(conn, sql3)
    ibm_db.execute(stmt3)
    account3 = ibm_db.fetch_assoc(stmt3)
    for x3 in account3.values():
        s3=x3
    return render_template("dashboardfinal.html",ye=s1,yes=s,cate=s2,pro=s3)
@app.route('/supplier.html')
def supply():
    return render_template("supplier.html")
@app.route('/employee_details.html')
def employee():
    return render_template("/employee_details.html")

@app.route('/categories.html')
def category():
    return render_template("/categories.html")
@app.route('/login.html')
def signout():
    return render_template("/login.html")
@app.route('/product.html')
def productfinal():
    data = []
    s=[]
    s1=[]
    data1=[]
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
    return render_template("/product.html",data=s,data1=s1)
if __name__ =='__main__':
    app.run(debug=True)
