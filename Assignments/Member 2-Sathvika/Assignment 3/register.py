from flask import Flask,render_template,request
app=Flask( __name__ )
@app.route('/',methods=["GET","POST"])
def home():
    if request.method=="POST":
        uname=request.form.get("user")
        em=request.form.get("email")
        phn=request.form.get("phone")
        return render_template('display.html',uname=uname,em=em,phn=phn)
    return render_template('registeration.html')
if __name__=='__main__':
    app.run(debug=True)