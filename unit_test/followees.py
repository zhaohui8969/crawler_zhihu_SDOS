# coding=utf-8
import requests
import zhihuURL
from bs4 import BeautifulSoup

__author__ = 'natas'

TEMP_FILE = 'tmp.txt'


class Zhihu:
    def __init__(self):
        """
        初始化Cookie
        :rtype : object
        """
        self.cookiesStr = ''
        with open('zhihu.cookie', 'r')as f:
            self.cookiesStr = f.read()
        # 处理cookie格式
        self.coockiDic = dict(map(lambda x: x.split('=', 1), self.cookiesStr.split('; ')))
        self._session = requests.session()
        self._session.cookies.update(self.coockiDic)
        # 设置http头部
        self._session.headers.update({'X-Requested-With': 'XMLHttpRequest',
                                      'Referer': 'http://www.zhihu.com',
                                      'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                                    'rv:39.0) Gecko/20100101 Firefox/39.0',
                                      'Host': 'www.zhihu.com'})

    def getfollowers(self, username):
        """
        获取用户的followers
        :param username:string 用户名(URL)
        :return:list followers
        """
        url = zhihuURL.folloers(username)
        followers = {}
        print('url:' + url)
        # 用requests重写(为了session的复用)
        r = self._session.get(url)
        html = r.content
        # 临时保存一份html
        with open(TEMP_FILE, 'w') as f:
            f.write(html)
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
    zhobj = Zhihu()
    testuser = u'littleviper'
    followers = zhobj.getfollowers(testuser)
    print("followers count: %d" % (len(followers)))


if __name__ == '__main__':
    main()
