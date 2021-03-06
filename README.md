# Mars-Mission-Web-Scraping
A web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. 

To run this scraping code yourself, download this repository and run `app.py` in terminal.

Note: this code requires MongoDB to scrape and store the data. 

To view an example of the rendered template without running the scrape code, open the `test.html` file (contained in the templates folder) in Google Chrome. 

Explanations of the code can be found within each script. 

## Step 1 - Scraping

### NASA Mars News

* Scraped the [NASA Mars News Site](https://mars.nasa.gov/news/) and collected the latest News Title and Paragraph Text. 

* Assigned the text to variables for later reference.

```python
# Example:
news_title = "NASA's Mars Helicopter Completes Flight Tests"

news_p = "The first helicopter to fly on Mars had its first flight on Earth."
```

### JPL Mars Space Images - Featured Image

* Visited the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).

* Used splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.

```python
# Example:
featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
```

### Mars Weather

* Visited the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scraped the latest Mars weather tweet from the page. 

* Saved the tweet text for the weather report as a variable called `mars_weather`.

```python
# Example:
mars_weather = 'InSight sol 145 (2019-04-24) low -98.1ºC (-144.6ºF) high -19.3ºC (-2.8ºF) winds from the SW at 4.4 m/s (9.8 mph) gusting to 11.6 m/s (26.1 mph) pressure at 7.40 hPapic.twitter.com/aNZiH2H1Pm'
```

### Mars Facts

* Visited the Mars Facts webpage [here](http://space-facts.com/mars/) and used Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

* Used Pandas to convert the data to a HTML table string.

### Mars Hemispheres

* Visited the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.

Note: you need to click each of the links to the hemispheres in order to find the image url to the full resolution image.

* Saved both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Used a Python dictionary to store the data using the keys `img_url` and `title`.

* Appended the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

```python
# Example:
hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    {"title": "Cerberus Hemisphere", "img_url": "..."},
    {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    {"title": "Syrtis Major Hemisphere", "img_url": "..."},
]
```

- - -

## Step 2 - MongoDB and Flask Application

Used MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

### Process

* Create Python script called `scrape_mars.py` with a function called `scrape` that will execute all of the scraping code from above and return one Python dictionary containing all of the scraped data.

* Next, create a route called `/scrape` that will import the `scrape_mars.py` script and call the `scrape` function.

  * Store the return value in Mongo as a Python dictionary.

* Create a root route `/` that will query the Mongo database and pass the mars data into an HTML template to display the data.

* Create a template HTML file called `index.html` that will take the mars data dictionary and display all of the data in the appropriate HTML elements. 



