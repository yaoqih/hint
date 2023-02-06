# -*- coding: utf-8 -*-
'''
Created on 2016-12-13

@author: hustcc
@fix: yaoqi
'''
from __future__ import absolute_import
from hint import hint, utils,parsing
from hint.utils import error_solution
from hint.detector.error import errors as errors_describe

__version__ = '1.0.4_fix'

def check(text, ignore='', format='json', fn='anonymous',file_dir=None,format_output=None):
    '''check markdown text'''
    paragraphs=text.split('\n')
    err_ignore=[]
    for paragraph in range(len(paragraphs)):
        while 1:
            tokens = parsing.tokenizer(paragraphs[paragraph])
            errors = parsing.detect_errors(tokens, paragraphs[paragraph])
            errors=utils.ignore_errorcode(errors, ignore)
            for error in range(len(errors)-1,-1,-1):
                if f'{errors[error].code}|{errors[error].index}' in err_ignore:
                    errors.pop(error)
            if len(errors)>0:
                fix_text=error_solution(errors[0])
            else:
                break
            select=input("是否修复错误？(y/n)")
            if select=='y':
                paragraphs[paragraph]=fix_text
            elif select=='n' and f'{errors[0].code}|{errors[0].index}' not in err_ignore:
                err_ignore.append(f'{errors[0].code}|{errors[0].index}')
    if format_output and file_dir:
        with open('.'.join(file_dir.split('.')[:-1]+['_fix']+[file_dir.split('.')[-1]]),'w',encoding='utf-8') as target_f:
            target_f.write('\n'.join(paragraphs))
    # check results
    errors = hint.check(text)
    # ignores
    errors = utils.ignore_errorcode(errors, ignore)
            
    # format output array / dict
    errors = {fn: utils.format_errors(errors, format)}
    if format != 'json':
        errors = ['File:%s\n%s' % (k, '\n'.join(es))
                  for k, es in errors.items()
                  if len(es) > 0]
        errors = '\n\n'.join(errors)
    return errors


def check_file(fn, ignore='', format='json',format_output=True):
    '''check markdown file'''
    with open(fn,encoding='utf-8') as f:
        text = f.read()
        return check(text, ignore, format, fn=fn,format_output=format_output,file_dir= fn)
