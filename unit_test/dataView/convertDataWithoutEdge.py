# coding=utf-8
"""
转换数据格式到eCharts格式，去除掉边缘叶子节点
"""
import json
import sys

SRCFILE = 'test.json'
SRCFILE = sys.argv[1]

nodes = []
links = []


def main():
    fopen = open(SRCFILE, 'r')

    for item in fopen.readlines():
        nodes.append(json.loads(item)['u'])

    fopen.seek(0)
    for eachline in fopen.readlines():
        lineStr = json.loads(eachline)
        # 先处理 node
        u = lineStr['u']
        for eachF in lineStr['f']:
            if eachF in nodes:
                links.append(
                    {
                        'source': nodes.index(u),
                        'target': nodes.index(eachF),
                        'weight': 0.1
                    }
                )

    # 格式化输出
    output = {}
    output["type"] = "force"
    output["title"] = SRCFILE
    output["categories"] = [
        {
            "name": "HTMLElement",
            "keyword": {},
            "base": "HTMLElement",
            "itemStyle": {
                "normal": {
                    "brushType": "both",
                    "color": "#D0D102",
                    "strokeColor": "#5182ab",
                    "lineWidth": 1
                }
            }
        }]
    output["nodes"] = []
    output["links"] = []
    for item in nodes2dic(nodes):
        output["nodes"].append(item)
    output["links"] += links

    print(json.dumps(output))


def nodes2dic(nodes):
    """
    格式化nodes
    """
    for item in nodes:
        yield {
            "name": item,
            # "value": 1,
            "category": 1
        }


if __name__ == '__main__':
    main()
