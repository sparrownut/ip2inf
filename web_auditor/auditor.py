# coding=utf-8
# --------------------------------------------------------------------------
# Web界面审计
import re


def web_audit(text):  # web界面审计函数 要从中提取关键信息
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    text = text.replace('\t', '')
    text = text.replace('\x00', '')
    title = re.findall('<title>(.*?)</title>', text)
    if title is not None:
        pass
    body = re.findall('<body>(.*?)</body>', text)
    if body is not None:
        pass
