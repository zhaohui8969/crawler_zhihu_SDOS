# coding=utf-8
# 环路测试，因为在爬行的过程中不可避免的会出现环路（用户直接、间接互相关注），
# 因此需要解决环路问题

from pybloomfilter import BloomFilter

__author__ = 'natas'

DATA = {1: {2, 3},
        2: {3, 4},
        3: None,
        4: {1}}

bf = BloomFilter(10000000, 0.01, 'filter.bloom')


def traver(point):
    print(point)
    bf.add(point)
    if not DATA[point] is None:
        for nextPoint in DATA[point]:
            if nextPoint not in bf:
                traver(nextPoint)


def main():
    pass
    traver(1)


if __name__ == '__main__':
    main()
