import yagmail
import configparser
from news import NewsFeed

config = configparser.ConfigParser()
config.read('config.ini')


class Email:

    def generate_mail(self, name, articles:dict):
        """
        Create the mail body text by concatenate the titles and the links
        :param name: Username for greeting
        :param articles: Dictionary of title + link to the articles
        :return: The mail body text
        """
        mail_body = f'<h2 style="color:red;">Hey! {name} </h2>\n Here is some news for you &#128512:\n'
        for item in articles:
            mail_body = mail_body + item['title'] + ':\n' + \
                        f'<a href = "{item["link"]}" style>{item["link"]}</a>' +'\n\n'

        return mail_body

    def send_mail(self, mail_body, receiver):
        """
        Send single mail for single receiver using third-party package yagmail.
        :param mail_body: Text of the mail body.
        :param receiver: Mail address of the end user.
        :return: sending response.
        """
        connector = yagmail.SMTP(
            user = config['DEFAULT']['MAIL'],
            password = config['DEFAULT']['PASSWORD']
        )

        res = connector.send(
            to=receiver,
            subject='Your Daily Info Inside!',
            contents=mail_body
        )
        return res

    def send_newsfeed_to_users(self, frame, mail):
        """
        This method is about order the relevant data, and run the 'send_mail' method accordingly.
        It will iterate over the users data set (.xlsx file.), and for each record, create the mail, and send it out.
        :param frame: Data frame of users + mails + interests
        :param mail: mail entity to run the process
        :return: None
        """
        for idx, info in frame.iterrows():
            newsfeed = NewsFeed(info[2])
            items = newsfeed.extract_title_and_link(newsfeed.get())

            content = mail.generate_mail(name=info[0], articles=items)
            res = mail.send_mail(content, info[1])
            return res



