from news import  UsersInterestsExtractor
from emails import Email


def main():
    user = UsersInterestsExtractor()
    mail = Email()
    frame = user.read_manipulate_file('users.xlsx')
    mail.send_newsfeed_to_users(frame=frame, mail=mail)


if __name__ == '__main__':
    main()

