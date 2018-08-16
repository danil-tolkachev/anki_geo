import sys
import os

import requests
from lxml import html


def load_data(url, fname=None):
    if fname is None:
        fname = os.path.basename(url)
    if not os.path.exists(fname):
        r = requests.get(url, allow_redirects=True)
        open(fname, "wb").write(r.content)


def get_data(url, fname=None):
    load_data(url, fname)
    if fname is None:
        fname = os.path.basename(url)
    return open(fname, encoding="utf-8").read()


def country_id(flag_url):
    return int(flag_url.lstrip("/img/country/").rstrip("flag.png"))


def parse_seas(url, countries, f=sys.stdout):
    s = get_data(url)
    tree = html.fromstring(s)
    first = True
    for row in tree.xpath("//table/tr"):
        if first:
            first = False
            continue
        cols = row.xpath(".//td")
        img = cols[0].xpath(".//span/img/@src")[0]
        fname = img.lstrip("/img").replace("/", "_")
        load_data(
            os.path.dirname(url) + "/" + img, os.path.join("imgs", fname))
        names = list(cols[0].itertext())
        name0 = names[0].strip()
        if len(names) > 1:
            name1 = names[1].strip()
        else:
            name1 = ""
        area = cols[2].text.strip()
        depth = cols[3].text.strip()
        ocean = cols[4].text.strip()
        ids = list(map(country_id, cols[1].xpath(".//img/@src")))
        country_names = map(lambda id_: countries[id_], ids)
        country_names = ", ".join(country_names)
        print(
            name0,
            name1,
            ocean,
            f'<img src="{fname}">',
            area,
            depth,
            country_names,
            sep=";",
            file=f)


def parse_countries(url):
    s = get_data(url)
    tree = html.fromstring(s)
    first = True
    res = {}
    for row in tree.xpath("//table/tr"):
        if first:
            first = False
            continue
        cols = row.xpath(".//td")
        id_ = country_id(cols[0].xpath(".//img/@src")[0])
        name = cols[0].xpath(".//a/text()")[0]
        res[id_] = name
    return res


def main():
    res = parse_countries("https://geo.koltyrin.ru/strany_mira.php")
    res.update(
        parse_countries("https://geo.koltyrin.ru/strany_mira_zavisimye.php"))
    res.update(
        parse_countries(
            "https://geo.koltyrin.ru/strany_mira_nepriznannye.php"))
    parse_seas("https://geo.koltyrin.ru/morja.php", res,
               open('seas.txt', 'w', encoding='utf-8'))


if __name__ == "__main__":
    main()
