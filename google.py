import urllib.request
import urllib.parse
import json
import requests  # pip intasll requests
import execjs  # 安装指令：pip install PyExecJS
import random
import hashlib
import re
from reportlab.lib.pagesizes import A4
#from pdfgraph import Graphs
from reportlab.platypus import SimpleDocTemplate


class Py4Js():

    def __init__(self):
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072; 
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f"; 
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
    }; 
    function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
    } 
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


# 使用谷歌在线翻译方法：需要梯子
def google_translate(content):
    '''实现谷歌的翻译'''

    content = content.replace('\n', '')
    print(content)
    js = Py4Js()
    tk = js.getTk(content)
    if len(content) > 4891:
        return '输入请不要超过4891个字符！'
    param = {'tk': tk, 'q': content}
    result = requests.get("""http://translate.google.com/translate_a/single?client=t&sl=en 
        &tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss 
        &dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2""", params=param)
    # 返回的结果为Json，解析为一个嵌套列表
    print(result)
    trans = result.json()[0]
    res = ''
    for i in range(len(trans)):
        line = trans[i][0]
        if line != None:
            res += trans[i][0]

    return res


if __name__ == '__main__':
    res = google_translate("Your data engineering team is the backbone for ensuring data health. And, a modern data stack enables the data engineering team to continuously monitor data quality into the future")
    print(res)
    # create_pdf("t.pdf", "I am Chinese!Hello, everyone!"*20 + res*40)
    content = list()
    # content.append(Graphs.draw_title("I am Chinese"))
    # content.append(Graphs.draw_text(41 * "Hello, everyone."))
    # content.append(Graphs.draw_text(140 * "我是中国人，大家好!"))
    # 生成pdf文件
    doc = SimpleDocTemplate('report.pdf', pagesize=A4)
    doc.build(content)