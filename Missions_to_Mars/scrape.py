#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time


def scrape():
    #the url for the mars news site
    news_url = 'https://mars.nasa.gov/news'

    #activating splinter and making it headless so it runs in the background
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    #visiting the site and setting a sleep timer to let the page load
    browser.visit(news_url)
    time.sleep(3)

    #taking the html from the website
    news_html = browser.html
    #setting the parser
    soup1 = bs(news_html, 'lxml')
    # print(soup1.prettify())

    #finding the latest news title
    news_title_find = soup1.find('div', class_="content_title")
    news_title = news_title_find
    # news_title.text

    #finding the paragraph for the latest news
    news_p_find = soup1.find('div', class_ = "article_teaser_body")
    news_p = news_p_find.text
    # news_p

    #the url for the mars featured image
    mars_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    #visiting the url in the headless browser
    browser.visit(mars_image_url)
    #taking the html for that page
    img_html = browser.html
    #setting the parser for that page
    imgsoup = bs(img_html, 'lxml')
    # print(imgsoup.prettify())

    #finding the featured image
    featured_image = imgsoup.find('a', class_="button fancybox")

    #appending the domain name to the extracted url
    featured_image_url = 'https://www.jpl.nasa.gov'+ featured_image['data-fancybox-href']
    # featured_image_url

    #the url for the Mars weather twitter account
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'

    #visiting the twitter site and put a sleeper to let the page load
    browser.visit(mars_weather_url)
    time.sleep(3)

    #taking the html from that page
    weather_html = browser.html

    #setting the parser for that page
    weathersoup = bs(weather_html, 'lxml')
    # print(weathersoup.prettify())

    #pulling the tweets based on two different scenarios of how the page could be loaded
    mars_tweets = [weathersoup.find_all('p', class_="TweetTextSize"), weathersoup.find_all('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")]

    #whichever one actually has data will be the one we look through
    for tweets in mars_tweets:
        mars = tweets
    # print(mars)

    #checking to see if the latest tweet has the weather data. If it does, we set it to the variable mars_weather
    #and if it doesn't, we check the one before it
    for tweet in mars:
    #     print(tweet.text)
        if 'InSight' in tweet.text:
            mars_weather = tweet.text
            if tweet.a in tweet:
                mars_weather = mars_weather.strip(tweet.a.text)
            break
    # mars_weather

    #the url for the mars facts table
    mars_facts_url = 'https://space-facts.com/mars/'
    #visiting the site
    browser.visit(mars_facts_url)

    #using pandas to read for the tables on the page and taking the first one
    tables = pd.read_html(mars_facts_url)
    mars_table = tables[0]
    mars_table.rename(columns={0:'',1:'value'}, inplace=True)
    mars_facts = tables[0].to_html()
    # mars_facts

    #the url for the images of the mars hemispheres
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #visiting the page
    browser.visit(hemisphere_url)
    #taking the html for that page
    hemisphere_html = browser.html
    #setting the parser
    hemisphere_soup = bs(hemisphere_html, 'lxml')
    #pulling all the links from that page
    hemispheres = hemisphere_soup.find_all('a', class_="itemLink")
    # hemispheres[0].get('href')

    #setting a list to add the links and then appending the domain name to the beginning
    link_list = []
    for hemi in hemispheres:
        if hemi.get('href') not in link_list:
            link_list.append(hemi.get('href'))
    links = ['https://astrogeology.usgs.gov' + link for link in link_list]
    # links

    #setting a list and then cycling through the pages to pull the link for the image and then
    #adding it to the list, then adding them to a dictionary for later use
    hemisphere_image_urls = []
    for link in links:
        url = link
        browser.visit(url)
        
        mars_html = browser.html 
        soup = bs(mars_html, 'lxml')
        
        title_text = soup.find('h2', class_="title")
        img_url = soup.find('div', class_="downloads")
        
        hemidict = {'title': title_text.text, 'img_url': img_url.a.get('href')}
        hemisphere_image_urls.append(hemidict)
        




