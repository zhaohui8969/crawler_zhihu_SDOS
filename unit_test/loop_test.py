# coding=utf-8
# 环路测试，因为在爬行的过程中不可避免的会出现环路（用户直接、间接互相关注），
# 因此需要解决环路问题

from pybloomfilter import BloomFilter
import Queue
import traceback
import time

__author__ = 'natas'

DATA = {1: {2, 3},
        2: {3, 4},
        3: None,
        4: {1, 5},
        5: {6, 7},
        6: {7, 1, 8},
        7: {1, 2, 3},
        8: {1, 9},
        9: None}

# bf对象，在避免环路的时候用到
bf = BloomFilter(10000000, 0.01, 'filter.bloom')
# 一个队列，广度遍历的时候用到
queue = Queue.Queue()


def traver(point, maxdeep, q):
    # 初始化队列和bf
    q.put({'DC': 0})
    q.put(point)
    bf.add(point)
    deepnow = 0
    # 游览队列
    while True:
        # time.sleep(1)
        try:
            item = q.get(block=False)
            # 控制深度
            if not isinstance(item, int):  # 判断是不是深度控制标记
                deepnow = item['DC']
                print('deep:%d' % deepnow)
                q.put({'DC': deepnow + 1})
            else:
                # 处理节点
                point = item
                # print('node:%d' % point)
                # 用yield做迭代
                yield point
                # 达到最大深度，不再增加队列
                if deepnow == maxdeep:
                    break
                else:
                    # 未达到最大深度，继续添加队列
                    # 不是空节点
                    if DATA[point] is not None:
                        # 将未游览过的节点加入队列
                        for nextPoint in DATA[point]:
                            if nextPoint not in bf:
                                q.put(nextPoint)
                                bf.add(nextPoint)
                                # print('添加:%d' % nextPoint)

        except:
            traceback.print_exc()


def main():
    pass
    for i in traver(1, 2, queue):
        print i


if __name__ == '__main__':
    main()
