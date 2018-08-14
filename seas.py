import os

import requests
from lxml import html


def get_data(url):
    fname = os.path.basename(url)
    if os.path.exists(fname):
        return open(fname, encoding="utf-8").read()
    r = requests.get(url, allow_redirects=True)
    open(os.path.basename(url), "wb").write(r.content)
    return r.content


def country_id(flag_url):
    return int(flag_url.lstrip("/img/country/").rstrip("flag.png"))


def parse_seas(url, countries):
    s = get_data(url)
    tree = html.fromstring(s)
    first = True
    for row in tree.xpath("//table/tr"):
        if first:
            first = False
            continue
        cols = row.xpath(".//td")
        img = cols[0].xpath(".//span/img/@src")[0]
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
        country_names = " ".join(country_names)
        print(name0, name1, ocean, img, area, depth, country_names, sep=";")


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
    res.update(parse_countries("https://geo.koltyrin.ru/strany_mira_zavisimye.php"))
    res.update(parse_countries("https://geo.koltyrin.ru/strany_mira_nepriznannye.php"))
    from pprint import pprint

    pprint(res)
    parse_seas("https://geo.koltyrin.ru/morja.php", res)


if __name__ == "__main__":
    main()
