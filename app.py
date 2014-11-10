from flask import Flask, render_template, request, redirect, url_for, session, escape, flash
from functions import authenticate_user, find_user, create_user, update_user, nation_validity, query_validity, find_product, find_news, find_money

app=Flask(__name__)
app.secret_key = 'secret'


@app.route("/",methods=["GET","POST"])
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        button = request.form["b"]
        if button == "Login":
            validity = authenticate_user(username, password)
            if validity:
                session['username'] = username
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('register'))

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template("register.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        country = request.form["country"]
        currency = request.form["currency"]
        validity = nation_validity(country, currency)
        button = request.form["b"]
        if validity[0]:
            if button == "Register":
                t = create_user(username, password, country, currency)
                if (t[0] == True):
                    flash(validity[1])
                    return redirect(url_for('login'))
                else:
                    flash(t[1])
                    return redirect(url_for('register'))
        else:
            flash(validity[1])
            return redirect(url_for('register'))

@app.route("/home",methods=["GET","POST"])
def home():
    if request.method=="GET":
        if (session["username"] == ""):
            flash("You must be logged in to access this feature")
            return redirect(url_for('login'))
        else:
            return render_template("home.html")
    else:
        button = request.form["b"]
        if button == "Submit":
            amount = request.form["amount"]
            year = request.form["year"]

            item = request.form["item"]
            item = item.replace(' ', '')
            item = item.replace("'", "")
            validity = query_validity(amount, year, item)

            username = session["username"]
            user = find_user(username)
            nation = user["country"]
            currency = user["currency"]

            if validity == "Valid":
                #uses currency deflator api to find your money (and your price range) in 2009 dollars
                ans = find_money(amount, currency, year, nation)

                #Find the ebay products at that price
                results = find_product(ans, item)
                price = results[0]
                link = results[1]
                pic = results[2]

                l = [ans, price, link, pic]
                flash(l)
                return redirect(url_for("answer"))
            else:
                return render_template("home.html")
        if button == "Update":
            return redirect(url_for("update"))
        if button == "News":
            username = session["username"]
            user = find_user(username)
            currency = user["currency"]
            news = find_news(currency)
            flash(news)
            return redirect(url_for("news"))
        if button == "Logout":
            flash("You've been logged out")
            session["username"] = ""
            return redirect(url_for("login"))

@app.route("/update",methods=["GET","POST"])
def update():
    if request.method=="GET":
        if (session["username"] == ""):
            flash("You must be logged in to access this feature")
            return redirect(url_for('login'))
        else:
            return render_template("update.html")
    else:
        button = request.form["b"]
        if button == "Update":
            value = request.form.getlist('check')
            for val in value:
                v = request.form["%s" %(val,)]
                l = {"%s" % (val,): v}
                print("updating")
                update_user(session['username'],l)
            return redirect(url_for("home"))
        else:
            return redirect(url_for("home"))

@app.route("/news", methods=["GET","POST"])
def news():
    if request.method=="GET":
        if (session["username"] == ""):
            flash("You must be logged in to access this feature")
            return redirect(url_for('login'))
        else:
            return render_template("news.html")
    else:
        return redirect(url_for("home"))

@app.route("/answer", methods=["GET","POST"])
def answer():
    if request.method=="GET":
        if (session["username"] == ""):
            flash("You must be logged in to access this feature")
            return redirect(url_for('login'))
        else:
            return render_template("answer.html")
    else:
        return redirect(url_for("home"))


if __name__=="__main__":
    app.debug = True
    app.run()
