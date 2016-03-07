# coding=utf-8
import requests
import zhihuURL
import json
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
        self.head = zhihuURL.DEAFULT_HEADER.copy()
        self._session.headers.update(self.head)

    def xsrf(self, soup):
        """获取知乎的反xsrf参数

        :return: xsrf
        :rtype: str
        """
        return soup.find('input', attrs={'name': '_xsrf'})['value']

    def hash_id(self, soup):
        """获取作者的内部hash id

        :return: 用户hash id
        :rtype: str
        """
        div = soup.find('div', class_='zm-profile-header-op-btns')
        if div is not None:
            return div.button['data-id']
        else:
            ga = soup.find('script', attrs={'data-name': 'ga_vars'})
            return json.loads(ga.text)['user_hash']

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
        # 过滤出内容，分析页面的Ajax过程重写了这个部分
        hashid = self.hash_id(soup)
        xsrfstr = self.xsrf(soup)
        headers = dict(zhihuURL.DEAFULT_HEADER)
        headers['Referer'] = url
        params = {"order_by": "created", "offset": 0, "hash_id": hashid}
        data = {'_xsrf': xsrfstr, 'method': 'next', 'params': ''}
        gotten_date_num = 20
        offset = 0
        while gotten_date_num == 20:
            params['offset'] = offset
            data['params'] = json.dumps(params)
            res = self._session.post(zhihuURL.API_More_Followers_URL, data=data, headers=headers)
            json_data = res.json()
            gotten_date_num = len(json_data['msg'])
            offset += gotten_date_num
            for html in json_data['msg']:
                soup = BeautifulSoup(html, 'lxml')
                h2 = soup.find('h2')
                author_name = h2.a.text
                author_url = h2.a['href']
                followers[author_name] = {'author_url': author_url}
        return followers


def main():
    zhobj = Zhihu()
    # testuser = u'littleviper'
    testuser = u'zhao-hui-36-5'
    followers = zhobj.getfollowers(testuser)
    print("followers count: %d" % (len(followers)))


if __name__ == '__main__':
    main()
