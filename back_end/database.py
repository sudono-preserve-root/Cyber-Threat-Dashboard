import os
import psycopg2 as db 
from dotenv import load_dotenv, dotenv_values
from datetime import datetime

def connect_to_database() -> None:
    connection = None
    load_dotenv()
    try:
        params = {
            "host": os.getenv("SERVER"),
            "database": os.getenv("DATABASE"),
            "user": os.getenv("USER"),
            "password": os.getenv("PASSWORD"),
            "port": os.getenv("PORT")
        }
        connection = db.connect(**params)
        return connection
    except db.DatabaseError as error:
        print(f'An error has occurred: {error}')
        return None

def create_tables(connection: object) -> None:
    table_scripts =[
    """
        CREATE TABLE IF NOT EXISTS publishers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS articles (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            severity_level VARCHAR(20) NOT NULL,
            link TEXT UNIQUE NOT NULL,
            publisher_id INT REFERENCES publishers(id),
            published_date TIMESTAMP,
            description TEXT
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS tags (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS article_tags (
            article_id INT REFERENCES articles(id) ON DELETE CASCADE,
            tag_id INT REFERENCES tags(id) ON DELETE CASCADE,
            PRIMARY KEY (article_id, tag_id)
        );
    """ ]
    
    try:
        cursor = connection.cursor()
        for command in table_scripts:
            cursor.execute(command)
            connection.commit()
        cursor.close()
    except db.DatabaseError as error:
        print(f"An error has occurred creating the tables: {error}")

def insert_articles(articles: list, connection: object) -> None:
    try:
        cursor = connection.cursor()
        for article in articles:
            articles_table_check_duplicate_link_query = "SELECT link from articles WHERE link = %s;"
            cursor.execute(articles_table_check_duplicate_link_query, (article['link'],))
            duplicate_check_result = cursor.fetchone()
            if duplicate_check_result == None:
                articles_table_insert_query = "INSERT INTO articles (title, severity_level, link, publisher_id, published_date, description) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"
                publisher_table_insert_query = "INSERT INTO publishers (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id;"
                publisher_table_select_query = "SELECT id from publishers WHERE name = %s;"
                tag_table_insert_query = "INSERT INTO tags (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id;"
                tag_table_select_query = "SELECT id from tags WHERE name = %s;"
                article_tags_insert_query = "INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s);"

                cursor.execute(publisher_table_select_query, (article['source'],))
                publisher_check = cursor.fetchone()
                if publisher_check:
                    publisher = publisher_check[0]
                else:
                    cursor.execute(publisher_table_insert_query, (article['source'],))
                    publisher = cursor.fetchone()[0]

                cursor.execute(articles_table_insert_query, (article['title'], article['severity'], article['link'], publisher, article['date'], article['description'],))
                article_id = cursor.fetchone()[0]

                for tag in article['tags']:
                    cursor.execute(tag_table_select_query, (tag,))
                    tag_check = cursor.fetchone()
                    if tag_check:
                        tag_id = tag_check[0]
                    else:
                        cursor.execute(tag_table_insert_query, (tag,))
                        tag_id = cursor.fetchone()[0]
                    cursor.execute(article_tags_insert_query, (article_id, tag_id,))
            else:
                continue
        connection.commit()
    except db.DatabaseError as error:
        print(f"An error has occured inserting articles: {error}")
    finally:
        if connection:
            print('Closing connection')
            connection.close()

def retrieve_articles(connection: object, offset: int = 0, limit: int = 0, level: str = None) -> list[dict]:
    try:
        cursor = connection.cursor()
        select_articles_query = "SELECT * FROM articles ORDER BY id DESC, published_date DESC LIMIT %s OFFSET %s;"
        select_articles_by_threat_severity_query = "SELECT * FROM articles WHERE severity_level = %s ORDER BY id DESC, published_date DESC LIMIT %s OFFSET %s;"
        select_publisher_query = "SELECT name FROM publishers WHERE id = %s;"
        select_tag_ids_query = "SELECT tag_id FROM article_tags WHERE article_id = %s;"
        select_tag_query = "SELECT name FROM tags WHERE id = %s;"
        if level:
            cursor.execute(select_articles_by_threat_severity_query, (level, limit, offset))
        else:
            cursor.execute(select_articles_query, (limit, offset))
        rows = cursor.fetchall()
        articles = []
        for row in rows:
            article_id = row[0]
            print(article_id)
            article_title = row[1]
            article_severity = row[2]
            article_link = row[3]
            publisher_id = row[4]
            article_publish_date = str(row[5]).split(' ')[0].split('-')
            date_format = datetime(year = int(article_publish_date[0]), month = int(article_publish_date[1]), day = int(article_publish_date[2]))
            article_publish_date = date_format.strftime("%B %d, %Y")
            article_description = row[6]

            cursor.execute(select_publisher_query, (publisher_id,))
            
            article_publisher = cursor.fetchone()[0]

            cursor.execute(select_tag_ids_query, (article_id,))
            tag_ids = cursor.fetchall()
            
            article_tags = []
            for tag in tag_ids:
                tag = tag[0]
                cursor.execute(select_tag_query, (tag,))
                article_tags.append(cursor.fetchone()[0])
            
            data = {
                "title": article_title,
                "description": article_description,
                "publisher": article_publisher,
                "date": article_publish_date,
                "tags": article_tags,
                "severity": article_severity,
                "link": article_link
            }
            articles.append(data)
        return articles
    
    except db.DatabaseError as error:
        print(f"An error has occurred retrieving articles: {error}")
    finally:
        if connection:
            print('closing connection')
            connection.close()

def retrieve_analytics(connection: object) -> dict:
    try:
        cursor = connection.cursor()
        get_row_number_query = "SELECT COUNT(*) FROM articles;"
        get_specific_severity = "SELECT COUNT(*) FROM articles WHERE severity_level = %s;"

        cursor.execute(get_row_number_query)
        row_number = cursor.fetchone()[0]

        cursor.execute(get_specific_severity, ("Low",))
        low_severity_threat_number = cursor.fetchone()[0]

        cursor.execute(get_specific_severity, ("Medium",))
        medium_severity_threat_number = cursor.fetchone()[0]

        cursor.execute(get_specific_severity, ("High",))
        high_severity_threat_number = cursor.fetchone()[0]

        critical_severity_threat_number = row_number - (low_severity_threat_number + medium_severity_threat_number + high_severity_threat_number)

        data = {
            'total': row_number,
            'low': low_severity_threat_number,
            'medium': medium_severity_threat_number,
            'high': high_severity_threat_number,
            'critical': critical_severity_threat_number
        }

        return data
        
    except db.DatabaseError as error:
        print(f"an error has occured retrieving the analytic data: {error}")
    finally:
        if connection:
            print('closing connection')
            connection.close()

def retrieve_monthly_analytics(connection: object, years: list[int] = [datetime.now().year], months: list[int] = []) -> dict:
    try:
        cursor = connection.cursor()
        month_dic = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                    5: 'May', 6: 'June', 7: 'July', 8: 'August', 
                    9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        months.sort()
        years.sort()
        data = {}

        select_month_data_query = "SELECT COUNT(*) FROM articles WHERE EXTRACT(YEAR FROM published_date) = %s AND EXTRACT(MONTH FROM published_date) = %s;"
        
        for year in years:
            if months:
                for month in months:
                    if type(month) != int:
                        raise TypeError('The months list must contain integer elements')
                    elif month < 1 or month > 12:
                        raise ValueError('month must be within the range 1-12')
                    cursor.execute(select_month_data_query, (year, month,))
                    month_name = month_dic[month]
                    key = f"{month}-{month_name}-{year}"
                    data[key] = cursor.fetchone()[0]
            else:
                for month in range(1,13):
                    cursor.execute(select_month_data_query, (year, month,))
                    month_name = month_dic[month]
                    key = f"{month}-{month_name}-{year}"
                    data[key] = cursor.fetchone()[0]
        
        return data
    except db.DatabaseError as error:
        print(f"An error has occurred retrieving monthly analytic data: {error}")
    finally:
        if connection:
            print('Closing connection')
            connection.close()

def retrieve_tag_analytics_specific(connection: object, tags: list[str] = [], years: list[int] = [datetime.now().year], months: list[int] = []) -> dict:
    try:
        cursor = connection.cursor()
        months.sort()
        years.sort()

        select_all_tags_query = "SELECT * FROM tags;"
        select_specific_tags = "SELECT id FROM tags WHERE name = %s;"
        select_articles_by_tag_and_year = """
        SELECT id
        FROM articles, article_tags
        WHERE article_tags.tag_id = %s AND article_tags.article_id = articles.id AND EXTRACT(YEAR FROM articles.published_date) = %s;
        """
        select_articles_by_tag_year_and_month = """
        SELECT id
        FROM articles, article_tags
        WHERE article_tags.tag_id = %s AND article_tags.article_id = articles.id AND EXTRACT(YEAR FROM articles.published_date) = %s AND EXTRACT(MONTH FROM articles.published_date) = %s;
        """
        
        month_dic = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                    5: 'May', 6: 'June', 7: 'July', 8: 'August', 
                    9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        
        queried_tags = []
        if not tags:
            cursor.execute(select_all_tags_query)
            queried_tags = cursor.fetchall()
        else:
            for tag in tags:
                cursor.execute(select_specific_tags, (tag,))
                tag_id = cursor.fetchone()
                if tag_id:
                    queried_tags.append((tag_id[0], tag))
        
        data = {}
        for year in years:
            if months:
                for month in months:
                    if type(month) != int:
                        raise TypeError('The months list must contain integer elements')
                    elif month < 1 or month > 12:
                        raise ValueError('month must be within the range 1-12')
                    for tag in queried_tags:
                        cursor.execute(select_articles_by_tag_year_and_month, (tag[0], year, month,))
                        key = f"{tag[1]}-{month_dic[month]}-{year}"
                        article_count = cursor.fetchall()
                        if article_count:
                            data[key] = len(article_count)
                        else:
                            data[key] = 0
            else:
                for tag in queried_tags:
                    cursor.execute(select_articles_by_tag_and_year, (tag[0], year,))
                    key = f"{tag[0]}-{tag[1]}-{year}"
                    article_count = cursor.fetchall()
                    if article_count:
                        data[key] = len(article_count)
                    else:
                        data[key] = 0
        return data
    except db.DatabaseError as error:
        print(f"An error has occurred retrieving tag analytic data: {error}")
    finally:
        if connection:
            print('closing connection')
            connection.close()

def retrieve_years(connection: object) -> list:
    try:
        cursor = connection.cursor()
        select_all_years = "SELECT DISTINCT EXTRACT(YEAR FROM published_date) FROM articles"
        cursor.execute(select_all_years)
        dates = (cursor.fetchall())
        dates_list = []
        for date in dates:
            dates_list.append(int(date[0]))
        return dates_list
    except db.DatabaseError as error:
        print(f'An error has occurred retrieving the years of the data: {error}')