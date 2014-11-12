
import json, urllib2
from pymongo import MongoClient

#MongoDB
client = MongoClient('localhost', 27017)
db = client.mongo_project
users = db.users

#some helper methods

###METHODS FOR THE USER'S INFO###

#Checks that the provided username password combo is in the databases
def authenticate_user(username, password):
    user = find_user(username)
    # No such user
    if user == None:
        return False
    # Username/Password combo don't match
    elif str(user['username']) != username or str(user['password']) != password:
        return False
    # We good
    else:
        return True

#Finds the user in the database based on the username. That user can then be manipulated in other functions
def find_user(username):
    user = users.find_one({'username': username})
    return user

#Adds a user to the database. Returns a tuple of whether it was successful and a message to be flashed. Assumes a valid country and currency (already checked in nation_validity method)
def create_user(username, password, country, currency):
        res = db.users.find({'username':username})
        if res.count() != 0:
            return (False,"Username taken")
        else:
            user = {
                'username' : username,
                'password' : password,
                'country' : country,
                'currency': currency,
            }
            users.insert(user)
            return (True, "User added")

# Updates a given field in the user's info, update_dict must be in the form {field_to_update : new_val}.
def update_user(username, update_dict):
        db.users.update({'username' : username}, {'$set' : update_dict}, upsert=False)
        return True


###METHODS TO PREVENT UNUSABLE INFO FROM BEING INPUTTED INFO###


#check's the user's country and currency against the useable ones for the currency deflator api
def nation_validity(nation, currency):
    nations = ["AUS", "AUT", "BEL", "BRA", "CAN", "CHE", "CHL", "CHN", "COL", "CZE", "DEU", "DNK", "ESP", "EST", "FIN", "FRA", "GBR", "GRC", "HUN", "IND", "ISR", "ITA", "JPN", "KOR", "KWT", "LTU", "LUX", "LVA", "NLD", "NOR", "NZL", "POL", "PRT", "SAU", "SVK", "SWE", "THA", "TWN", "USA", "ZAF"]
    if (nation in nations) == False:
        return (False, "Nation invalid")
    currencies = ["AED", "AMD", "BIF", "BTN", "CAD", "CHF", "CNY", "COP", "CZK", "DJF", "EEK", "EGP", "ERN", "ETB", "EUR", "GBP", "GHS", "GNF", "HKD", "HUF", "INR", "KES", "KMF", "KRW", "KWD", "LRD", "LSL", "LTL", "LVL", "LYD", "MAD", "MGA", "MRO", "MUR", "MWK", "NAD", "NGN", "NZD", "PLN", "RWF", "SAR", "SDG", "SKK", "THB", "TND", "TZS", "UGX", "USD", "XAF", "XOF", "ZAR", "ZMK"]
    if (currency in currencies) == False:
         return (False, "Currency invalid")
    else:
        return (True, "User Registered")

def nation_currency(string):
    nations = ["AUS", "AUT", "BEL", "BRA", "CAN", "CHE", "CHL", "CHN", "COL", "CZE", "DEU", "DNK", "ESP", "EST", "FIN", "FRA", "GBR", "GRC", "HUN", "IND", "ISR", "ITA", "JPN", "KOR", "KWT", "LTU", "LUX", "LVA", "NLD", "NOR", "NZL", "POL", "PRT", "SAU", "SVK", "SWE", "THA", "TWN", "USA", "ZAF"]
    currencies = ["AED", "AMD", "BIF", "BTN", "CAD", "CHF", "CNY", "COP", "CZK", "DJF", "EEK", "EGP", "ERN", "ETB", "EUR", "GBP", "GHS", "GNF", "HKD", "HUF", "INR", "KES", "KMF", "KRW", "KWD", "LRD", "LSL", "LTL", "LVL", "LYD", "MAD", "MGA", "MRO", "MUR", "MWK", "NAD", "NGN", "NZD", "PLN", "RWF", "SAR", "SDG", "SKK", "THB", "TND", "TZS", "UGX", "USD", "XAF", "XOF", "ZAR", "ZMK"]
    if string == "nations":
        return nations
    else:
        return currencies

#helper method to make sure a useable date, year, and item were inputed. The amount must be a whole number, the year must be between 1975 and 2009 (the date range for which our api has data)
def query_validity(amount, year, item):
    if (year.isdigit() == False):
        return "y must be a number"
    y = int(year)
    if (y < 1975):
        return "Year too low"
    if (y > 2009):
        return "Year too high"
    if (amount.isdigit() == False):
        return "Amount must be a number"
    if (item == ""):
        return "You forgot the item"
    else:
        return "Valid"


###METHODS THAT QUERY THE APIS###

#uses currency deflator api to find your money in 2009 dollars
def find_money(amount, currency, year, nation):
     url = "https://data.itpir.wm.edu/deflate/api.php?val=%s%s%s%s"
     url = url%(amount, currency, year, nation)
     req = urllib2.urlopen(url)
     result = req.read()
     ans = json.loads(result)
     return ans

#Finds a list of products using the ebay api, sends back the product link with the price closest to how much money the user has
def find_product(ans, item):
    #Ebay api returns list of items and prices
    url = "http://open.api.ebay.com/shopping?appid=CobyGold-0d75-4e41-993d-a4faa8a54198&version=517&siteid=0&callname=FindItems&itemFilter(0).name=MinPrice&itemFilter(0).value=(%s)&itemFilter(1).name=MaxPrice&itemFilter(1).value=(%s)&QueryKeywords=%s&responseencoding=JSON"
    url = url%(item)
    req = urllib2.urlopen(url)
    d = req.read()
    result = json.loads(d)
    dif = -1
    price = 0
    link = ""
    pic = ""
    for r in result['Item']:
        p = r["ConvertedCurrentPrice"]["Value"]
        l = r["ViewItemURLForNaturalSearch"]
        if dif == -1:
            price = p
            link = l
            pic = r["GalleryURL"]
            dif = abs(p - ans)
        else:
            #print "discarding: " + p
            if (dif > abs(p - ans)):
                #print "old price: " + price
                #print "new price: " + p
                price = p
                dif = abs(p - ans)
                link = l
                pic = r["GalleryURL"]
    return [price, link, pic]


#finds the news on the currency using the google news api, sends back a list of links about the currency
def find_news(currency):
    url= "https://ajax.googleapis.com/ajax/services/search/news?v=1.0&q=%s&userip=5000"
    currency = currency + "currency"
    url = url%(currency)
    req = urllib2.urlopen(url)
    result = req.read()
    results = result.split("unescapedUrl")
    ret = []
    for res in results:
        #each news item has unescapedUrl, split there
        x = res.find("unescapedUrl")
        #find the url that follows unescapedUrl
        r = res[x+10:x+200]
        #Since urls have varying lengths, cut at the ,
        x = r.find(",")
        r = r[1:x-1]
        #To avoid localhost being attached as the prefix
        r = "http://" + r
        ret.append(r)
    ret = ret[1:len(ret)]
    for r in ret:
        if r[0] != 'w':
            ret.remove(r)
    return ret
