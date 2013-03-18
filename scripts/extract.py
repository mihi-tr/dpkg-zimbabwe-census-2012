import scraperwiki
import lxml.html
import re
import itertools
import csv

filename="../data/CensusPreliminary2012.pdf"

startpage=17
endpage=117

def get_province(page):
  txt=(i.text_content().strip() for i in page.cssselect("text"))
  for t in txt:
    if "PROVINCE" in t:
      (number,name)=re.search("=[ ]*([0-9]+)[ ]*([A-Za-z ]+)",t).groups()
      return (int(number),name.strip())
  return (None,None)


def get_district(page):
  txt=(i.text_content().strip() for i in page.cssselect("text"))
  for t in txt:
    if "DISTRICT" in t:
      (number,name)=re.search("=[ ]*([0-9]+)[ ]*([A-Za-z ]+)",t).groups()
      return (int(number),name.strip())
  return None,None


def to_float(item):
  try:
    return float(item.replace(" ","").replace(",","."))
  except ValueError:
    return None

def get_totals(page):
  els=(i.text_content() for i in page.cssselect("text[font='20']"))
  return map(to_float, re.split("[  ]{2,}","  ".join([i for i in
  itertools.ifilter(to_float, els)]).strip()))

def get_page(root,number):
  return root.cssselect("page[number='%s']"%number)[0]

def get_content(page):
  return [i for i in itertools.chain(get_province(page),
  get_district(page), get_totals(page))]

def get_root(filename):
  f=open(filename,"rb")
  return lxml.html.fromstring(scraperwiki.pdftoxml("".join(f)))


if __name__=="__main__":
  root=get_root(filename)
  pages=map(lambda x: get_page(root,x), range(startpage,endpage))
  f=open("../data/population.csv","wb")
  w=csv.writer(f)
  w.writerow(["Province Number","Province","District Number","District","Males","Females",
  "Total Population","Households","Average Persons per Household"])
  for p in pages:
    w.writerow(get_content(p))
  f.close()
