import requests
import bs4
import os
from tqdm import tqdm

sitemap = requests.get("https://iuk.one/sitemap.xml").text

soup = bs4.BeautifulSoup(sitemap, "html.parser")

# find all loc tags
loc_tags = soup.find_all("loc")

links = []
for tag in loc_tags:
    link = tag.text
    links.append(link)


def downloads_all_pdfs(link):
    site_name = link.split("/")[-1].split(".")[0]

    response = requests.get(link)

    
    li_tags = bs4.BeautifulSoup(response.text, "html.parser").find_all("li")

    pdf_tups = [] #name, link
    for tag in li_tags:
        a_tag = tag.find("a")
        if a_tag:
            name = tag.find("b")
            name = str(name).replace("<b>", "").replace("</b>", "")
            pdf_tups.append((name, a_tag.get("href")))
    
    pdf_tups = [(name, link) for name, link in pdf_tups if ".pdf" in link]

    os.makedirs(os.path.join("downloads", site_name), exist_ok=True)

    for name, pdf_link in tqdm(pdf_tups):

        if pdf_link.startswith("/"):
            pdf_link = "https://iuk.one" + pdf_link
        else:
            pdf_link = "https://iuk.one/" + pdf_link

        name = name.replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace("\"", "_").replace("<", "_").replace(">", "_").replace("|", "_").replace(" ", "_")

        if not name.endswith(".pdf"):
            name += ".pdf"

        with open(os.path.join("downloads", site_name, name), "wb") as f:
            f.write(requests.get(pdf_link).content)
        
    if len(pdf_tups) == 0 and len(os.listdir(os.path.join("downloads", site_name))) == 0:
        os.rmdir(os.path.join("downloads", site_name))
    
    print(f"Downloaded {len(pdf_tups)} pdfs from {link}")

for link in links:
    downloads_all_pdfs(link)