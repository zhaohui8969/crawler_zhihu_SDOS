# coding=utf-8
import textwrap

__author__ = 'natas'

main_help = r'''
            这个用法：python2.7 ./crawler.py <user> <depth>

            参数的说明：
            <user>：用户的知乎id，你可以从URL中得到，举个例子，这位用户的主页

                  https://www.zhihu.com/people/huo-zhen-bu-lu-zi-lao-ye

                  user的值就是huo-zhen-bu-lu-zi-lao-ye

            <depth>：设置爬虫的深度，可以理解为关系链要爬多长，不建议太大
            '''


def print_help():
    print(textwrap.dedent(main_help))
