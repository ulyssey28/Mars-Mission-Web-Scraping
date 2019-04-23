# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars_app")



# create route that renders index.html template
@app.route("/")
def index():
    mars = mongo.db.mars_news.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scraper():
    news = mongo.db.mars_news
    mars_data = scrape_mars.scrape()
    news.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
