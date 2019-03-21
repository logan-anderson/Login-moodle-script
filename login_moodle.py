import requests
from bs4 import BeautifulSoup
from slackclient import SlackClient

#############################################################
'''
    this is where you enter your username and password and slack token
'''
course_id = ""
user = ""
psw = ""
token = ''
soup = ''


#############################################################

def slack_message(message, channel):
    """
    :param message:  the message you want to send in your slack channel
    :param channel: the channel you want the message on
    :return: N/A
    """
    global token
    sc = SlackClient(token)
    sc.api_call('chat.postMessage',
                channel=channel,
                text=message,
                username='',
                icon_emoji=':robot_face:')


def get_soup():
    """
    this method gets the html from moodle and returns it in a bs4 object
    """
    global soup
    session = requests.Session()

    payload = {
        'username': user,
        'password': psw
    }
    session.post('https://moodle31.upei.ca/login/index.php', data=payload)
    # website = session.get("https://moodle31.upei.ca/course/view.php?id=" + course_id)
    url = 'https://moodle31.upei.ca/grade/report/user/index.php?id= ' + course_id
    website = session.get(url)
    html = website.text
    soup = BeautifulSoup(html, "html.parser")


def check_grade(this_id):
    """
    this method writes the table into the text file and also checks for changes
    :param this_id: the id you want to check the grade for
    """
    global course_id
    course_id = this_id
    get_soup()
    table_text = soup.find('table').text
    try:
        f = open(course_id + "_old_table_text", "r")
        temp = f.read()
        if temp == table_text:
            print('no update for course with id= ' + course_id)
        else:
            print('update for course with id' + course_id)
            slack_message('grade updated for class id= ' + course_id, '#social')
        f.close()
        f = open(course_id + "_old_table_text", "w")
        f.write(table_text)
        f.close()
    except FileNotFoundError:
        f = open(course_id + "_old_table_text", "w")
        f.write(table_text)
        f.close()


# check all the grades (this could also be done in a loop)
check_grade('4718')
check_grade('4732')
check_grade('4734')
check_grade('5039')
