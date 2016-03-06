__author__ = 'natas'

PEOPLE_URL = ['https://www.zhihu.com/people/']


def followees(uername):
    return PEOPLE_URL[0] + uername + '/followees'


def folloers(username):
    return PEOPLE_URL[0] + username + '/followers'
