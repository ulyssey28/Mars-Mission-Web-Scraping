# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import time
import pandas as pd



def scrape():
##########################################################################################################################################################
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
##########################################################################################################################################################
# Mars News (NASA Website)
##########################################################################################################################################################
     # URL of NASA page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # using the .visit() method tell the browser to visit the url
    browser.visit(url)

    #sleep code to allow browser page to load
    time.sleep(5)

    #obtain the page html using the .html attribute of the browser object
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    #Collect the latest News Title and Paragraph Text. 
    #Note the find method gets the first "div" tag with class = "content_title", corresponding to the latest news title 
    news_title_tag =  soup.find("div", class_="content_title")
    news_title = news_title_tag.text

    #Collect full news article link
    news_path = news_title_tag.a["href"]
    news_link = "https://mars.nasa.gov"+ news_path

    news_paragraph_tag = soup.find("div", class_="article_teaser_body")
    news_paragraph = news_paragraph_tag.text
##########################################################################################################################################################
# JPL Mars Space Images - Featured Image
##########################################################################################################################################################
    #Scrape latest featured image from Mars from NASA website
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # using the .visit() method tell the browser to visit the url
    browser.visit(img_url)

    #sleep code to allow browser page to load
    time.sleep(5)

    #obtain the page html using the .html attribute of the browser object
    featured_img_html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    img_soup = BeautifulSoup(featured_img_html, 'html.parser')

    #Find the <a> tag with id "full_image".. which contains a link to the featured image
    a_tag = img_soup.find("a", id="full_image")
    featured_img_link = a_tag["data-fancybox-href"]

    # The current string is: (/spaceimages/images/mediumsize/PIA17357_ip.jpg)

    # Create a variable called lg_featured_img_url which holds the full path to the image
    lg_featured_img_url = "https://www.jpl.nasa.gov" + featured_img_link

##########################################################################################################################################################
# Mars Weather (Twitter)
##########################################################################################################################################################
    #Scrape the latest Mars weather tweet from Mars Weather page
    twitter_url = "https://twitter.com/marswxreport?lang=en"

    # using the .visit() method tell the browser to visit the url
    browser.visit(twitter_url)

    #sleep code to allow browser page to load
    time.sleep(5)

    #obtain the page html using the .html attribute of the browser object
    twitter_html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    twitter_soup = BeautifulSoup(twitter_html, 'html.parser')

    # Examine twitter page html using inspector and find the div class which refers to the container for each tweet
    tweet_container = twitter_soup.find("div", class_="tweet")

    # Grab the text within the first paragraph of the container
    mars_weather = tweet_container.p.text

    # Replace the newline symbols within the string with spaces
    mars_weather = mars_weather.replace("\n", " ")
##########################################################################################################################################################
# Mars Facts
##########################################################################################################################################################
    # Use the read_html function in Pandas to automatically scrape any tabular data from a page.
    Marsfact_url = "https://space-facts.com/mars/"

    # Using the pandas .read_html() method, we can convert the html tables found the page to pandas dataframes.
    # Note the result of the .read_html() method is a list of dataframes pulled from the page.. In this case there is only one table
    url_tables = pd.read_html(Marsfact_url, encoding= "utf-8")

    # Reference the first element of our list of dataframes
    mars_facts_df = url_tables[0]

    # Rename Columns and set index
    mars_facts_df = mars_facts_df.rename(columns={0: "Description"})
    mars_facts_df = mars_facts_df.rename(columns={1: "Values"})
    mars_facts_df = mars_facts_df.set_index("Description")

    # Remove newline symbols and set html equal to the variable facts_html
    facts_html = mars_facts_df.to_html().replace('\n', '')

##########################################################################################################################################################
# Mars Hemispheres
##########################################################################################################################################################
    # Obtain high resolution images for each of Mar's hemispheres.
    hem_imgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # using the .visit() method tell the browser to visit the url
    browser.visit(hem_imgs_url)

    #sleep code to allow browser page to load
    time.sleep(5)

    #obtain the page html using the .html attribute of the browser object
    hem_html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    hem_soup = BeautifulSoup(hem_html, 'html.parser')

    # Create an empty list that will hold our image info dictionaries
    hemisphere_image_info = []

    # Create a list of "div"s of class="description"... which hold the information pertaining to our hemisphere titles
    soup_div_list = hem_soup.find_all("div", class_="description")



    """ The following code loops through our list of "divs" of class= "description".
    For each "div":
    1. We first make sure we are on the starting hem_imgs_url page 
    as we will be moving to several pages throughout the loop.

    2. We then time out our code as a precautionary measure since transitioning from page to page 
    may require the browser to load at times

    3. We set the hem_title (hemisphere title) equal to the "h3" text found inside the current "div"

    4. We then transition to a new page with the splinter - click_link_by_partial_text() method using the hem_title as the argument
    since the link to the image page is connected to our hem_title text

    5. From there we obtain the html of the image page using the browser.html method

    6. We then create a soup object using the html

    7. From inspecting the html, the information of interest is contained within a "div" of class_="downloads". 
    We create a container object referencing the this "div"

    8. Then find the first <a> tag which corresponds to the sample image link and extract the href attribute which contains
    the link to the fullsized image

    9. We then create a dictionary with "title" and "img_url" keys that match with our hem_title and img_url values respectively.

    10. Lastly we append the dictionary to our hemisphere_image_info list
    """


    for div in soup_div_list:
        browser.visit(hem_imgs_url)

        #sleep code to allow browser page to load
        time.sleep(10)
        hem_title = div.find("h3").text
        try:
            browser.click_link_by_partial_text(hem_title)
            nxt_pg_html = browser.html
            
            nxt_pg_soup = BeautifulSoup(nxt_pg_html, 'html.parser')

    # Create a soup object for the "div" thats contains the content of interest.. in this case the <a> tags with image links
            container_div = nxt_pg_soup.find("div", class_="downloads")

    # Find the first <a> tag which corresponds to the sample image link and extract the href attribute
            img_url = container_div.a["href"]
            img_title_dict = {"title": hem_title, "img_url": img_url }
            
    # Append the dictionary to our hemisphere_image_info list
            hemisphere_image_info.append(img_title_dict)
        except:
            print("Scraping Complete")


    lastest_dict = {"news_link": news_link, "news_title": news_title, "news_paragraph": news_paragraph, "featured_img": lg_featured_img_url, "mars_weather" : mars_weather, "fact_table": facts_html, "hem_imgs": hemisphere_image_info}

    return lastest_dict

    

    

    

    
















