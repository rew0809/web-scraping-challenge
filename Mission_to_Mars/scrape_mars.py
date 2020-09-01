from bs4 import BeautifulSoup as bs
import requests
import os
from splinter import Browser
import pandas as pd
import time


def scrape():
    #Step 1 - Scraping
    #NASA Mars News

    #set up chrome extension
    executable_path = {'executable_path': 'C:/Users/rewel/Downloads/chromedriver_win32/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    url = 'https://mars.nasa.gov/news/'
    # Retrieve page with the requests module
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')

    #parse out latest News Title and Paragraph Text
    news_title = soup.find("section", class_="grid_gallery module list_view").find("div", class_="grid_layout").find("li", class_="slide").find("div", class_="content_title").find("a").text

    news_p = soup.find("div", class_="grid_layout").find("li", class_="slide" ).find("div", class_="article_teaser_body").text


    #setting up new soup instance for JPL site
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')


    #JPL Mars Space Images - Featured Image
    #scraping JPL mars site for featured image and building url
    featured_image_url = soup.find('a', class_="button fancybox")["data-fancybox-href"]
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url


    #Mars Facts
    #scraping table from Mars space facts site and storing as html string
    url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(url)
    mars_table = pd.DataFrame(mars_table[0])
    mars_table.columns = ["Description", "Mars"]
    mars_table = mars_table.set_index("Description")

    #converting data frame to html string
    mars_html = mars_table.to_html(classes= "str")


    #Mars Hemispheres
    marsHems = ['Cerberus', 'Syrtis_Major', 'Valles_Marineris', 'Schiaparelli']

    hemisphere_image_urls = []
    for hems in marsHems:
        
        url = f'https://astrogeology.usgs.gov/search/map/Mars/Viking/{hems}_enhanced'
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')

        imgLoc = soup.find('div', class_="downloads").find('a')['href']
        
        title = f'{hems} Hemisphere'
        
        #enter titles and image urls into dictionary
        hemisphere_data = {"title": title, "img_url": imgLoc}
        hemisphere_image_urls.append(hemisphere_data)

    mars_data = {"NewsTitle": news_title, "NewsPara": news_p, "FeaturedImg":featured_image_url, "MarsTable": mars_html, 
     "HemisphereData":hemisphere_image_urls }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data


def scrape_img():
    #set up chrome extension
    executable_path = {'executable_path': 'C:/Users/rewel/Downloads/chromedriver_win32/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #Mars Hemispheres
    marsHems = ['Cerberus', 'Syrtis_Major', 'Valles_Marineris', 'Schiaparelli']

    hemisphere_image_urls = []
    for hems in marsHems:
        
        url = f'https://astrogeology.usgs.gov/search/map/Mars/Viking/{hems}_enhanced'
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')

        imgLoc = soup.find('div', class_="downloads").find('a')['href']
        
        title = f'{hems} Hemisphere'
        
        #enter titles and image urls into dictionary
        hemisphere_data = {title: imgLoc}
        hemisphere_image_urls.append(hemisphere_data)

    # Close the browser after scraping
    browser.quit()

    # Return results
    return hemisphere_data