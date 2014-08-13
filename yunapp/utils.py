# -*- coding: utf-8 -*-
## Common function  or comman constans
import cgi

def show_site_map(rules, prefix=None):
    links = []
    support_method = set(['GET', 'POST', 'PUT', 'DELETE'])

    for rule in rules:
        method = support_method & rule.methods
        links.append((rule.rule, method.pop(), rule.endpoint))

    s = []
    s.append('<h2>Site Map</h2><table width="800"><tr><td width="20%"><b>Method</b>')
    s.append('</td><td><b>URI</b></td><td><b>Function</b></td></tr>')

    links = sorted(links, key=lambda link: (link[0], link[1]))
    if prefix is None:
        prefix = ''
    for url, method, name in links:
        print prefix+url
        s.append('<tr><td>[%s]</td><td><a href="%s" target="_blank">%s</a>'\
            '</td><td>%s</td></tr>' % (method, prefix+url, cgi.escape(url), name))

    s.append('</table>')
    return ''.join(s)