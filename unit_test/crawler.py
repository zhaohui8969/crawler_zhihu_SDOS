# coding=utf-8
# 爬虫从这里启动

import followees
from pybloomfilter import BloomFilter
import Queue
import traceback
import time
import json
import sys
import banner

__author__ = 'natas'

# bf对象，在避免环路的时候用到
bf = BloomFilter(100000000, 0.01, 'filter.bloom')
# 一个队列，广度遍历的时候用到
queue = Queue.Queue()

FILE_BUFF_LINE = 100


def crawfun(user_url, maxdeep, q, zhihuobj):
    # 初始化队列和bf
    q.put(0)
    q.put(user_url)
    deepnow = 0
    father = user_url  # 辅助记录当前节点的父节点

    # 游览队列
    while True:
        try:
            item = q.get(block=False)
            # 控制深度
            if isinstance(item, int):  # 判断是不是深度控制标记
                deepnow = item
                if deepnow > maxdeep:
                    break
                print('deep:%d' % deepnow)
                q.put(deepnow + 1)
            elif isinstance(item, dict):  # 判断是不是父节点辅助标记
                father = item['F']
            else:
                # 处理节点
                user_url = item
                relaDic = {'u': father, 'f': user_url}
                print(relaDic)
                # 用yield做迭代
                yield relaDic  # 返回用户以及他的一位followee
                # 达到最大深度，不再增加队列
                if deepnow < maxdeep:
                    print('continu...')
                    # 未达到最大深度，继续添加队列
                    # 获取follower列表
                    if user_url not in bf:
                        bf.add(user_url)
                        followeesList = zhihuobj.getfollowees(user_url)
                        if not followeesList == []:
                            q.put({'F': user_url})
                            for i in followeesList:
                                q.put(i)

        except:
            raise


def main():
    # 数据整合用到的临时变量
    lastuser = None
    tempdata = None

    # 初始化
    zhihuObj = followees.Zhihu()

    # 设置参数
    testuser1 = u'littleviper'
    testuser2 = u'zhao-hui-36-5'
    testuser3 = u'li-shou-peng-31'
    username = testuser2
    depth = 1

    # 获取一下console输入的参数
    arglen = len(sys.argv)
    if not ((arglen == 1) or (arglen == 3)):
        banner.print_help()
        exit()
    elif arglen == 3:
        username = sys.argv[1]
        depth = sys.argv[2]

    # 启动爬虫
    resJson = crawfun(username, depth, queue, zhihuObj)
    resJson.next()
    filename = "%s+%d+%s.json" % (username, depth, time.strftime('%Y%m%d-%H%M%S'))

    # 保存数据
    try:
        f = open(filename, 'w')
        lineCount = 0
        for i in resJson:
            # 刷新缓存
            if lineCount > FILE_BUFF_LINE:
                lineCount = 0
                f.flush()
            # 判断记录是否是和上一条属于同一个用户的
            if i['u'] == lastuser:
                tempdata['f'].append(i['f'])
            else:
                if tempdata is not None:
                    f.write(json.dumps(tempdata) + '\n')
                lastuser = i['u']
                tempdata = {'u': lastuser, 'f': [i['f']]}
            lineCount += 1
        f.write(json.dumps(tempdata) + '\n')
        f.close()
        print('Save to %s' % filename)
    except (KeyboardInterrupt, SystemExit) as e:
        # 处理按键终止程序
        f.close()
        print(e)
        print('Save to %s' % filename)
        print('Quit.')


if __name__ == '__main__':
    main()
