# coding=utf-8
# 环路测试，因为在爬行的过程中不可避免的会出现环路（用户直接、间接互相关注），
# 因此需要解决环路问题

from pybloomfilter import BloomFilter
import Queue
import traceback
import time

__author__ = 'natas'

DATA_old = {1: {2, 3},
            2: {3, 4},
            3: None,
            4: {1, 5},
            5: {6, 7},
            6: {7, 1, 8},
            7: {1, 2, 3},
            8: {1, 9},
            9: None}

DATA = {1: {2, 3},
        2: {4, 5},
        3: {6, 7},
        6: {8, 9},
        8: {1},
        9: {2}}

# bf对象，在避免环路的时候用到
bf = BloomFilter(10000000, 0.01, 'filter.bloom')
# 一个队列，广度遍历的时候用到
queue = Queue.Queue()


def traver(point, maxdeep, q):
    # 初始化队列和bf
    q.put({'DC': 0})
    q.put(point)
    # bf.add(point)
    deepnow = 0
    father = point  # 辅助记录当前节点的父节点
    # 游览队列
    while True:
        # time.sleep(0.1)
        try:
            item = q.get(block=False)
            # 控制深度
            if not isinstance(item, int):  # 判断是不是深度控制标记
                if 'F' in item:
                    father = item['F']
                else:
                    deepnow = item['DC']
                    if deepnow > maxdeep:
                        break
                    print('deep:%d' % deepnow)
                    q.put({'DC': deepnow + 1})
            else:
                # 处理节点
                point = item
                # print('node:%d' % point)
                # 用yield做迭代
                yield {father: point}
                # 未达到设定的深度，继续遍历
                if deepnow < maxdeep:
                    # 不是空节点
                    if point in DATA and DATA[point] is not None:
                        # 将未游览过的节点的子节点加入队列
                        if point not in bf:
                            bf.add(point)
                            q.put({'F': point})
                            for nextPoint in DATA[point]:
                                q.put(nextPoint)

        except:
            traceback.print_exc()
            break


def main():
    pass
    for i in traver(1, 10, queue):
        print(i)
        # print(queue.qsize())


if __name__ == '__main__':
    main()
