# -*- coding: utf-8 -*-
'''
Created on 2016-12-13

@author: hustcc
'''

errors = {
    # 空格
    'E101': u'英文与非标点的中文之间需要有一个空格',
    'E102': u'数字与非标点的中文之间需要有一个空格',
    'E103': u'全角标点与其他字符之间不加空格',
    'E104': u'除了％、℃、°、以及倍数单位（如 2x、3n）之外，数字与单位之间需要增加空格',
    # 标点符号
    'E201': u'不重复使用标点符号',
    'E202': u'只有中文或中英文混排中，一律使用中文全角标点',
    'E203': u'如果出现整句英文，则在这句英文中使用英文、半角标点',
    'E204': u'省略号请使用……标准用法',
    'E205': u'英文和后面的半角标点之间不需要空格',
    # 数字
    'E301': u'数字使用半角字符',
}


class Error(object):
    def __init__(self, text, code, index=0):
        self.text = text
        self.code = code
        self.index = index
        self.fix=None

    def description(self):
        return errors.get(self.code, 'unknow')

    def short_text(self, length=20):
        text_len = len(self.text)
        half_len = length // 2

        start = self.index - half_len
        start = start > 0 and start or 0

        end = start + length
        end = end > text_len and text_len or end

        return u'%s<%s>%s' % (self.text[start:self.index],
                              self.code,
                              self.text[self.index:end])

    def json_format(self):
        rst = {}
        rst['code'] = self.code
        rst['text'] = self.short_text()
        rst['index'] = self.index
        rst['description'] = self.description()
        return rst

    def text_format(self):
        return u'%s:COL<%s>:%s:"%s"' % \
            (self.code, self.index,
             self.description(), self.short_text())

    def format(self, format='text'):
        if format == 'json':
            return self.json_format()
        return self.text_format()


class BaseDetector(object):
    def __ini__(self):
        pass

    def errors(self):
        return []

    def find_all_string(self, str, sub):
        index = []
        i = 0
        while i != -1:
            i = str.find(sub, i + 1)
            if i == -1:
                return index
            else:
                index.append(i)

        return index
