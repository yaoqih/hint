# -*- coding: utf-8 -*-
'''
Created on 2016-12-13

@author: hustcc
'''
from __future__ import absolute_import
from hint import utils
import functools
import re
import sys


def pre_process(md_text):
    '''pre process the mark down text string.
    '''
    # 1. 去除代码块
    # md_text = re.sub(r'(```.*```)', '',
    #                  md_text, flags=re.I | re.S) 贪婪匹配，误删文件内容
    md_text = re.sub(r'```.*?(.*?)```', '',
                     md_text, flags=re.I | re.S)
    # 2. 删除图片
    md_text = re.sub(r'(\!\[.*?\]\(.*?\))', '', md_text, flags=re.I)
    # 3. 提取链接内容
    md_text = re.sub(r'\[(.*?)]\(.*?\)', '\g<1>', md_text, flags=re.I)
    # 4. 去除 ``
    md_text = re.sub(r'`(.*?)`', '\g<1>', md_text, flags=re.I)
    return md_text or u''


def to_paragraph_array(md_text):
    '''parse mark down file, and return all the paragraph array'''
    md_text = pre_process(md_text)
    # change to unicode
    if sys.version_info[0] == 3 and not isinstance(md_text, str):
        md_text = md_text.decode('utf-8')
    elif sys.version_info[0] == 2 and not isinstance(md_text, unicode):  # noqa
        md_text = md_text.decode('utf-8')

    md_lines = md_text.split('\n')
    # filter not empty element
    return [f'{line} |line|{md_lines[line]}' for line in range(len(md_lines))]


def reduce_handler(tokens, c):
    '''how to reduce to get token strings.'''
    type = utils.typeof(c)
    tokens.append({'type': type, 'text': c})
    return tokens


def tokenizer(p):
    '''parse each mark down text line, get the tokenizer of the line'''
    tokens = functools.reduce(reduce_handler, p, [])
    return tokens


def detect_errors(tokens, p):
    '''detect error code from tokens.'''
    errors = []
    # 自动加载所有的检测器
    detectors = utils.load_detectors()

    for detector in detectors:
        errors += errors + detector(tokens, p).errors()

    return errors
