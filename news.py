import requests
import pandas as pd
import configparser
from datetime import datetime, timedelta

config = configparser.ConfigParser()
config.read('config.ini')


class UsersInterestsExtractor:
    """Create users data frame, with multiple subjects as a list"""

    def read_manipulate_file(self, path):
        """
        Read the data, return it with subjects as list.
        :param path: Path to the data sheet
        :return: data with subjects as list
        """
        data = pd.read_excel(path)
        data['Interests'] = data['Interests'].apply(lambda x: x.split(','))
        return data


class NewsFeed:
    """Create the news feed object, to feed the mail body"""

    date_format = "%Y-%m-%d"
    today = datetime.now().strftime(date_format)
    yesterday = (datetime.now() - timedelta(days=1)).strftime(date_format)

    def __init__(self, interests):
        self.interests = [x.replace(" ","").lower() for x in interests] # For each subject: Lower case and remove blank
                                                                        # spaces

    def api_generator(self, query, api_key, start_date=yesterday, end_date=today, lan='en'):
        """
        Generate API call tp NewsApi
        :param query: Subject to search for
        :param api_key: NewsAPI personal token
        :param start_date: of the period, you want news from
        :param end_date: of the period, you want news from
        :param lan: Language
        :return: API call with all the query parameters
        """
        return f"https://newsapi.org/v2/everything?" \
               f"q={query}" \
               f"&language={lan}" \
               f"&from={start_date}" \
               f"&to={end_date}" \
               f"&apiKey={api_key}"

    def get(self, per_subject=5, start_date='2023-01-01', end_date='',
            api_key=config['DEFAULT']['APIKEY'], lan='en'):

        """
        Get list of news from the API
        :param per_subject: Limit the amount of articles per subject
        :param start_date: of the period, you want news from
        :param end_date: of the period, you want news from
        :param api_key: NewsAPI personal token
        :param lan: Language
        :return: List of articles
        """

        queries = [interest.lower() for interest in self.interests]
        responses = []
        for q in queries:
            url = self.api_generator(
                start_date=start_date,
                end_date=end_date,
                api_key=api_key,
                lan=lan,
                query=q
            )
            response = requests.get(url).json().get('articles')[:per_subject]
            responses.append((q, response))
        return responses

    def extract_title_and_link(self, subjects):
        """
        Extract only important information from the article attribute: title, link. subject.
        :param subjects: Articles list
        :return: Dictionary for each article with the information
        """
        titles_and_links = []
        for subject, articles in subjects:
            for article in articles:
                title = article.get('title')
                link = article.get('url')
                titles_and_links.append({'subject':subject,'title': title, 'link': link})
        return titles_and_links
