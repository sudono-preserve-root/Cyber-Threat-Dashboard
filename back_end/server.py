from flask import Flask, request
from flask_cors import cross_origin
from database import connect_to_database, insert_articles, retrieve_articles, retrieve_analytics, retrieve_monthly_analytics, retrieve_tag_analytics_specific
from web_scraper import scrape_cyber_security_dive, scrape_cyber_security_news, scrape_hacker_news, scrape_cyber_crime_magazine
from classification import extract_cves, extract_tags, determine_severity
import random
import json
app = Flask(__name__)

@app.route('/scrape_news_sources')
def scrape_news_sources():
    scraped_articles = []
    database_connection = connect_to_database()
    if database_connection:
        cyber_security_dive_list = [
        'https://www.cybersecuritydive.com/topic/breaches/', 'https://www.cybersecuritydive.com/topic/vulnerability/',
        'https://www.cybersecuritydive.com/topic/cyberattacks/', 'https://www.cybersecuritydive.com/topic/threats/']

        cyber_security_news_list = [
            'https://cybersecuritynews.com/category/threats/', 'https://cybersecuritynews.com/category/cyber-attack/', 
            'https://cybersecuritynews.com/category/vulnerability/', 'https://cybersecuritynews.com/category/data-breaches/']
        
        hacker_news_urls = ["https://thehackernews.com/","https://thehackernews.com/search/label/data%20breach",
                    "https://thehackernews.com/search/label/Cyber%20Attack", "https://thehackernews.com/search/label/Vulnerability"]
        
        for url in cyber_security_dive_list:
            scrape_cyber_security_dive(url = url, prefix= url, data = scraped_articles, max_pages = 3, current_page=1)

        for url in cyber_security_news_list:
            scrape_cyber_security_news(url = url, data = scraped_articles, max_pages = 3, current_page=1)

        for url in hacker_news_urls:
            scrape_hacker_news(url = url, data = scraped_articles, max_pages = 3, current_page=1)

        scrape_cyber_crime_magazine(url = 'https://cybersecurityventures.com/today/#cybercrime-magazine-today/', data = scraped_articles, prefix= 'https://cybersecurityventures.com/today/#cybercrime-magazine-today/', max_pages = 23, current_page=1)
        verified_articles = []
        for article in scraped_articles:
            CVES = extract_cves(title = article['title'], text = article['description'])
            article['tags'] = extract_tags(title = article['title'], text = article['description'], matched_tags= article['tags'])
            article['severity'] = determine_severity(tags = article['tags'], cves= CVES)
            for cve in CVES:
                article['tags'].append(cve)
            
            if article['tags']:
                verified_articles.append(article)
        
        random.shuffle(verified_articles)
        insert_articles(articles=verified_articles, connection = connect_to_database())

        return ("Scraping Successful", 200)
    return ("Scraping Unsuccessful", 500)

@app.route('/fetch_articles/<offset>/<limit>')
@app.route('/fetch_articles/<offset>/<limit>/<level>')
@cross_origin()
def fetch_articles(offset: int, limit: int, level: str = None) -> list[dict]:
    database_connection = connect_to_database()
    if database_connection:
        return json.dumps(retrieve_articles(connection= database_connection, offset = offset, limit = limit, level=level))
    else:
        return ("Fetching Unsuccessful", 500) 

@app.route('/fetch_analytic_data')
@cross_origin()
def fetch_analytical_data() -> dict:
    database_connection = connect_to_database()
    if database_connection:
        return json.dumps(retrieve_analytics(database_connection))
    else:
        return ("Fetching Unsuccessful", 500) 

@app.route('/fetch_monthly_analytics')
@app.route('/fetch_monthly_analytics/<years>')
@app.route('/fetch_monthly_analytics/<years>/<months>')
@cross_origin()
def fetch_monthly_statistic_data(years: str = None, months: str = None) -> dict:
    if years:
        years = years.split(',')
        for index in range(len(years)):
            years[index] = int(years[index])
    if months:
        months = months.split(',')
        for index in range(len(months)):
            months[index] = int(months[index])

    database_connection = connect_to_database()
    if database_connection:
        if not(years) and not(months):  
            return json.dumps(retrieve_monthly_analytics(database_connection))
        elif years and not(months):
            return json.dumps(retrieve_monthly_analytics(connection = database_connection, years = years))
        else:
            return json.dumps(retrieve_monthly_analytics(database_connection, years, months))
    else:
        return ("Fetching Unsuccessful", 500)


@app.route('/fetch_tag_analytics')
@app.route('/fetch_tag_analytics/<tags>')
@app.route('/fetch_tag_analytics/<tags>/<years>')
@app.route('/fetch_tag_analytics/<tags>/<years>/<months>')
@cross_origin()
def fetch_tag_statistic_data(tags: str = None, years: str = None, months: str = None) -> dict:
    
    if tags == 'skip':
        tags = None

    if tags and tags != 'skip':
        tags = tags.split(',')

    if years:
        years = years.split(',')
        for index in range(len(years)):
            years[index] = int(years[index])

    if months:
        months = months.split(',')
        for index in range(len(months)):
            months[index] = int(months[index])
    
    database_connection = connect_to_database()
    if not(tags) and not(years) and not(months):
        return json.dumps(retrieve_tag_analytics_specific(database_connection))
    elif tags and not(years) and not(months):
        return json.dumps(retrieve_tag_analytics_specific(connection = database_connection, tags = tags))
    elif tags and years and not(months):
        return json.dumps(retrieve_tag_analytics_specific(connection = database_connection, tags = tags, years = years))
    else:
        return json.dumps(retrieve_tag_analytics_specific(connection = database_connection, tags = tags, years = years, months= months))
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)