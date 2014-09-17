# -*- coding: utf-8 -*-
# # Common function  or comman constans
import cgi, hashlib, time
import logging

app_logger = logging.getLogger('yunapp')
business_logger = logging.getLogger('business')


def show_site_map(rules, prefix=None):
    links = list()
    support_method = set(['GET', 'POST', 'PUT', 'DELETE'])

    for rule in rules:
        method = support_method & rule.methods
        links.append((rule.rule, method.pop(), rule.endpoint))

    s = list()
    s.append('<h2>Site Map</h2><table width="800"><tr><td width="20%"><b>Method</b>')
    s.append('</td><td><b>URI</b></td><td><b>Function</b></td></tr>')

    links = sorted(links, key=lambda link: (link[0], link[1]))
    if prefix is None:
        prefix = ''
    for url, method, name in links:
        s.append('<tr><td>[%s]</td><td><a href="%s" target="_blank">%s</a>'
                 '</td><td>%s</td></tr>'
                 % (method, prefix + url, cgi.escape(url), name))

    s.append('</table>')
    return ''.join(s)


def get_int_page_num(page_num):
    if page_num.isdigit():
        page_num = int(page_num)
    else:
        page_num = 1
    return page_num