from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_bookmarks(elements):
    bms = []
    for el in elements.children:
        if el.name == "dt":
            if el.h3 is not None:
                # it is folder
                folder_title = el.h3.string
                folder_children = el.find_next("dl")
                bms.append({
                    "title": folder_title,
                    "children": get_bookmarks(folder_children),
                    "type": "folder"
                });
            elif el.a is not None:
                #it is link
                link_title = el.a.string
                link_url = el.a["href"]
                bms.append({
                    "title": link_title,
                    "url": link_url,
                    "type": "bookmark"
                });
    return bms

def make_url_markdown(url):
    return f"* [{url['title']}](url['url'])\n"

def make_folder_markdown(folder, hierarchy=2):
    md = ""
    for i in range(0, hierarchy):
        md += "#"
    print(md)
    md += f" {folder['title']} \n\n"

    for child in folder["children"]:
        if child["type"] == "folder":
            md += make_folder_markdown(child, hierarchy+1)
        else:
            md += make_url_markdown(child)
    
    md += "\n\n"
    return md

def make_markdown(bms):
    md = "# Links\n"

    materiais_bm = []

    for bm in bms:
        if bm["title"] == "Materias":
            materiais_bm = bm
            break

    for bm in materiais_bm["children"]:
        if bm["type"] == "folder":
            md += make_folder_markdown(bm)
        else:
            md += make_url_markdown(bm)

    return md

def main():
    file = open("favoritos_10_03_2019.html", "rb")
    html_string = file.read()

    bms = get_bookmarks(BeautifulSoup(html_string, "html5lib").body.dl.dl)
    md = make_markdown(bms)

    readme = open("README.md", "wb")
    readme.write(md.encode("utf-8"))

main()
