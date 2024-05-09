from flask import Flask, render_template, request, redirect, url_for

from flask_mysqldb import MySQL

from datetime import datetime

app = Flask(__name__)


app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Ackiran1999@"
app.config["MYSQL_DB"] = "expenditure_manager"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"



mysql = MySQL(app)


#total_amount = 2000
#history = []
@app.route("/delete/<string:id>")
def delete(id):
    # getting transaction history from history table with id
    con = mysql.connection.cursor()
    sql = "select * from history where id=%s"
    con.execute(sql, [id])
    history = con.fetchall()
    #print(history)
    

    # getting amount from money table
    sql = "select * from money"
    con.execute(sql)
    res = con.fetchall()
    #print(res)
    amount_id = res[0]["id"]
    amount = res[0]["amount"]
    #print(amount)

    # updating amount in money table
    query = ""
    if history[0]["status"] == "Debited" :
        query ="update money set amount = %s + %s where id=%s"
    else :
        query = "update money set amount = %s - %s where id=%s"
    sql = query
    con.execute(sql,[amount, history[0]["amount"], amount_id])
    mysql.connection.commit()

    # deleting transaction history with id
    sql = "delete from history where id=%s"
    con.execute(sql, [id])
    mysql.connection.commit()

    return redirect(url_for("home"))


@app.route("/", methods =["GET","POST"])
def home():
    global total_amount
    con = mysql.connection.cursor()
    if request.method == "POST" :
        date = request.form["Date"]
        category = request.form["Category"]
        ownCategory = request.form["ownCategory"]
        status = request.form["Status"]
        user_amount = request.form["Amount"]
        print(date, category, status, user_amount)
        category = category
        if len(ownCategory) > 0:
            category = ownCategory

        date_object = datetime.strptime(date, "%Y-%m-%d")
        # formatted_date = date_object.strftime("%d-%m-%Y")
        # print("date")
        # print(date_object)

        # adding transaction in history table

        sql = "insert into history(transactionDate, category, status, amount) values(%s, %s, %s, %s);"
        con.execute(sql,[date_object, category, status, int(user_amount)])
        mysql.connection.commit()
        

        # getting amount from money table
        sql = "select * from money"
        con.execute(sql)
        res = con.fetchall()
        # print(res)
        id = res[0]["id"]
        amount = res[0]["amount"]
        # print(amount)


        # updating amount in money table

        query = ""
        if status == "Debited" :
            query ="update money set amount = %s - %s where id=%s"
        else :
            query ="update money set amount = %s + %s where id=%s"

        sql = query
        con.execute(sql,[amount, int(user_amount), id])
        mysql.connection.commit()
        
        
        # history.append({"date": date, "category": category, "status": status, "amount": amount})
        # if status == "Debited" :
        #     total_amount = total_amount - int(amount)
        # else :
        #     total_amount = total_amount + int(amount)

    # getting amount from money table

    sql = "select * from money"
    con.execute(sql)
    res = con.fetchall()
    # print(res)
    amount = res[0]["amount"]
    # print(amount)

    # getting transaction history from history table 
    
    sql = "select * from history"
    con.execute(sql)
    history = con.fetchall()
    for i in history:
        #print(i)
        i["transactionDate"] = i["transactionDate"].strftime("%d-%m-%y")
    print(history)

    return render_template("home.html",data=[amount, history] )



if (__name__ == '__main__'):
    app.run(debug=True)