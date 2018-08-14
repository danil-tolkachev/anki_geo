from lxml import html
import requests
import os


def get_data(url):
    fname = os.path.basename(url)
    if os.path.exists(fname):
        return open(fname, encoding="utf-8").read()
    r = requests.get(url, allow_redirects=True)
    open(os.path.basename(url), "wb").write(r.content)
    return r.content


def parse_seas():
    s = get_data("https://geo.koltyrin.ru/morja.php")
    tree = html.fromstring(s)

    first = True
    for row in tree.xpath("//table/tr"):
        if first:
            first = False
            continue
        cols = row.xpath(".//td")
        img = cols[0].xpath(".//span/img/@src")[0]
        name = cols[0].text_content().strip().split("\n")
        name0 = name[0].strip()
        if len(name) > 1:
            name1 = name[2].strip()
        else:
            name1 = ""
        area = cols[2].text.strip()
        depth = cols[3].text.strip()
        ocean = cols[4].text.strip()
        countries = map(
            lambda s: s.lstrip("/img/country/").rstrip("flag.png"),
            cols[1].xpath(".//img/@src"),
        )
        countries = " ".join(countries)
        print(name0, name1, ocean, img, area, depth, countries, sep=";")


def main():
    parse_seas()


if __name__ == "__main__":
    main()
