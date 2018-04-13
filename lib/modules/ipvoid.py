#!/usr/bin/env python
##
# omnibus - deadbits.
# ipvoid module
##
import BeautifulSoup

from http import http_get

from common import is_ipv4


def run(ip):
    result = {}
    if not is_ipv4(ip):
        return None

    headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}
    url = 'http://ipvoid.com/scan/%s/' % ip
    try:
        status, response = http_get(url, headers=headers)
    except:
        return result

    if status:
        data = BeautifulSoup(response.text)

        if data.findAll('span', attrs={'class': 'label label-success'}):
            return None

        elif data.findAll('span', attrs={'class': 'label label-danger'}):
            for each in data.findAll('img', alt='Alert'):
                site = each.parent.parent.td.text.lstrip()
                url = each.parent.a['href']
                result[site] = url

    return result


def main(artifact, artifact_type=None):
    result = run(artifact)
    return result
