from flask import Flask, render_template, request


app = Flask(__name__)

total_amount = 2000
history = []

@app.route("/", methods =["GET","POST"])
def home():
    global total_amount
    if request.method == "POST" :
        date = request.form["Date"]
        category = request.form["Category"]
        status = request.form["Status"]
        amount = request.form["Amount"]
        print(date, category, status, amount)
        history.append({"date": date, "category": category, "status": status, "amount": amount})
        if status == "Debited" :
            total_amount = total_amount - int(amount)
        else :
            total_amount = total_amount + int(amount)
    return render_template("home.html",data=[total_amount, history] )



if (__name__ == '__main__'):
    app.run(debug=True)