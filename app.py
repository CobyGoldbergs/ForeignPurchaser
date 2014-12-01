from flask import Flask, render_template, request, redirect, url_for, session, escape, flash
from functions import authenticate_user, find_user, create_user, update_user, nation_validity, query_validity, find_product, find_news, find_money, nation_currency

app=Flask(__name__)
app.secret_key = 'secret'

#do my commits work

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
                flash("Username or password was invalid")
                return redirect(url_for('login'))
        else:
            return redirect(url_for('register'))

@app.route("/register",methods=["GET","POST"])
def register():
    nations = nation_currency("nations")
    currencies = nation_currency("currencies")
    if request.method=="GET":
        return render_template("register.html", nations=nations, currencies=currencies)
    else:
        button = request.form["b"]
        if button == "Login":
            return redirect(url_for('login'))
        username = request.form["username"]
        password = request.form["password"]
        country = (request.form["country"])[0:3]
        print "cou " + country
        currency = (request.form["currency"])[0:3]
        print "cur " + currency
        validity = nation_validity(country, currency)
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
            #print "currency: " + currency
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
                flash("One or more of your forms was invalid")
                return render_template("home.html")

@app.route('/logout')
def logout():
    flash("You've been logged out")
    session["username"] = ""
    return redirect(url_for("login"))

@app.route("/update",methods=["GET","POST"])
def update():
    nations = nation_currency("nations")
    currencies = nation_currency("currencies")
    if request.method=="GET":
        if (session["username"] == ""):
            flash("You must be logged in to access this feature")
            return redirect(url_for('login'))
        else:
            return render_template("update.html", nations=nations, currencies=currencies)
    else:
        button = request.form["b"]
        if button == "Update":
            value = request.form.getlist('check')
            for val in value:
                v = request.form["%s" %(val,)]
                if (val == "country") or (val == "currency"):
                    v = v[0:3]
                l = {"%s" % (val,): v}
                flash("Updated")
                update_user(session['username'],l)
            return redirect(url_for("home"))
        else:
            return redirect(url_for("update"))

@app.route("/news", methods=["GET","POST"])
def news():
    username = session["username"]
    user = find_user(username)
    currency = user["currency"]
    print currency
    news = find_news(currency)
    if request.method=="GET":
        if (session["username"] == ""):
            flash("You must be logged in to access this feature")
            return redirect(url_for('login'))
        else:
            print news
            display = None
            if not news:
                display = "Sorry, looks like there's no news for your currency."
            return render_template("news.html", news = news, display = display)
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

