__author__ = 'natas'

PEOPLE_URL = ['https://www.Zhihu.com/people/']

zhihuURL = r'https://www.zhihu.com'


def followees(uername):
    return PEOPLE_URL[0] + uername + '/followees'


def folloers(username):
    return PEOPLE_URL[0] + username + '/followers'


API_More_Followers_URL = zhihuURL + '/node/ProfileFollowersListV2'

DEAFULT_HEADER = {'X-Requested-With': 'XMLHttpRequest',
                  'Referer': 'http://www.zhihu.com',
                  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                'rv:39.0) Gecko/20100101 Firefox/39.0',
                  'Host': 'www.zhihu.com'}
