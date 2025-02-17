from bs4 import BeautifulSoup
from glob import glob

files_loc = "../seanlabean.github.io/site/*"
good_text = []
files = glob(files_loc)
for f in files:
    html = open(f).read()
    soup = BeautifulSoup(html, "html.parser")
    # Remove <figure> and <img> tags
    for tag in soup(["figure", "img", "li", "ol", "ul"]):
        tag.decompose()

    page_txt = soup.prettify().split() # list of str 
    # want to get all lines after <p> (which may be it's own element or the first characters of the element we want)
    # I believe this can be left as and concatenated into a single long string.
    add = False
    for i, l in enumerate(page_txt):
        if add == True and l[0] != "<" and l[-1] != ">":
            good_text.append(page_txt[i])
        if l == "<p>":
            add = True
        if i < len(page_txt)-1 and page_txt[i+1] == "</p>":
            add = False

        # elif l[:2] == "<p>" and len(l) > 3:
        #     good_text.append(l[3:len(l)-3])
    out_text = ' '.join(good_text)
print(out_text)