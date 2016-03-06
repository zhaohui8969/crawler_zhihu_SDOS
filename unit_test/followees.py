# coding=utf-8
import urllib2
import zhihuURL
from bs4 import BeautifulSoup

__author__ = 'natas'

COOKIES = ''
TEMP_FILE = 'tmp.txt'


def init():
    """
    初始化Cookie
    """
    global COOKIES
    COOKIES = open('zhihu.cookie', 'r').read()


def getfollowers(username):
    """
    获取用户的followers
    :param username:string 用户名(URL)
    :return:list followers
    """
    url = zhihuURL.folloers(username)
    followers = {}
    print('url:' + url)
    opener = urllib2.build_opener()
    opener.addheaders = []
    opener.addheaders.append(('Cookie', COOKIES))
    opener.addheaders.append((('User-agent',
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) '
                               'AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/49.0.2623.75 Safari/537.36')))
    html = opener.open(url).read()
    fopen = open(TEMP_FILE, 'w')
    fopen.write(html)
    # print(html)
    soup = BeautifulSoup(html, 'lxml')
    # 过滤出内容
    zm_profile_section_wrap = soup.find(attrs={'class': ['zm-profile-section-wrap']})
    followerstag = zm_profile_section_wrap.findAll('h2')
    if len(followerstag) > 0:
        for i in followerstag:
            username = i.a.get('title')
            userurl = i.a.get('href')
            print("%s\t%s" % (username, userurl))
            followers[username] = userurl
    return followers


def main():
    init()
    testuser = u'littleviper'
    followers = getfollowers(testuser)
    print("followers count: %d" % (len(followers)))


if __name__ == '__main__':
    main()
