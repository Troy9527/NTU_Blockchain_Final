import os, csv, bs4, re, sys, io, numpy
import urllib.request
import googlemaps
from PIL import Image
import requests

def search_div(string, div):
    index = -1

    for i in range(len(div)):
        if string in div[i]:
            index = i
            break
            
    return index

def parsing_transac(transac):
    ret = ""

    for i in range(len(transac)):
        temp = ""
        temp = re.sub(r"^[\t\s]+", "", transac[i].text)
        temp = re.sub(r"[\t\s]+$", "", temp)
        ret += temp + ","

    ret = ret[:-1]
    return ret

def parsing_GPS(text):
    ret = ""
    ret2 = ""
    colors = ["black", "brown", "green", "purple", "yellow", "blue", "gray", "orange", "red", "white"]
    _color = 0

    find = 0
    f = io.StringIO(text)
    l = []
    for line in f:
        if "];" in line:
            find = 0

        if find == 1:
            temp = re.sub(r"^[\t\s]+", "", line)
            temp = re.sub(r"[\t\s]+$", "", temp)
            temp = temp.split(",", 1)
            
            ret2 += "markers=color:" + str(colors[_color]) + "|" + temp[0][6:] + "," + temp[1][6:-1].strip('}') + "&"
            temp = "(" + temp[0][6:] + "," + temp[1][6:-1].strip('}') + ")"
            #l.append([float(temp[0][6:], float(temp[1][6:-1]))])

            ret += temp + ","
            _color = (_color + 1) % 10

        if "loc_arr[" in line and "] = [" in line:
            find = 1

    ret = ret[:-1]
    if not ret:
        ret = "None"
    return ret, ret2[:-1]

if __name__=='__main__':

    logno = sys.argv[1]

    html_bytes = urllib.request.urlopen('https://fc.efoodex.net/portal.php?oid=' + str(logno) + '&m=1').read()
    html_decode = html_bytes.decode('utf-8')

    soup = bs4.BeautifulSoup(html_decode, "lxml")

    oid = logno

    
    #gmaps = googlemaps.Client(key='AIzaSyCeFF-xV0ELuCP0IVkrzG5ahZgeA08hb3c')

    '''
    # remove prefix and training whitespaces
    product_name = soup.find_all("meta")[6]["content"]
    print(product_name)
    
    # parsing_info

    #div_block = soup.find_all("div", class_="username")[0].text.strip().split("\n")
    div_block = soup.find_all("div", class_="username")[0].text
    div_block = re.sub(r"^[\t\s]+", "", div_block, flags = re.MULTILINE)
    div_block = re.sub(r"[\t\s]+$", "", div_block, flags = re.MULTILINE)
    div_block = re.sub(r"[\t\s]+ \(", " (", div_block, flags = re.MULTILINE)
    div_block = div_block.split("\n")
   
    organization = "None"
    produce_date = "None"
    expired_date = "None"
    produce_amount = "None"
    remaining = "None"

    organization_index = search_div("產出組織", div_block)
    produce_date_index = search_div("產出日期", div_block)
    expired_date_index = search_div("有效日期", div_block)
    produce_amount_index = search_div("產出數量", div_block)
    remaining_index = search_div("剩餘數量", div_block)

    if organization_index != -1:
        organization = div_block[organization_index][5:]
    if produce_date_index != -1:
        produce_date = div_block[produce_date_index][5:]
    if expired_date_index != -1:
        expired_date = div_block[expired_date_index][5:]
    if produce_amount_index != -1:
        produce_amount = div_block[produce_amount_index][5:]
    if remaining_index != -1:
        remaining = div_block[remaining_index][5:]

    #print(organization)
    #print(produce_date)
    #print(expired_date)
    #print(produce_amount)
    #print(remaining)
    '''

    # parsing transaction
    transac = soup.body.find_all('a', class_='btn btn-dark btn-lg btn-width')
    num = len(transac)
    transac_str = parsing_transac(transac)

    print("Number of 作業: " + str(num))
    print(transac_str)

    

    # parsing GPS
    GPS, geocode = parsing_GPS(html_decode)
    print(GPS)
    
    zoom_level = 19

    while GPS != "None":
        center = geocode.split('&')[0].split('|')[1]

        map_url = "https://maps.googleapis.com/maps/api/staticmap?" + str(center) + "&size=1200x1200&zoom=" + str(zoom_level) + "&" + geocode + "&key=AIzaSyCeFF-xV0ELuCP0IVkrzG5ahZgeA08hb3c"


        map_bytes = requests.get(map_url)
        img = Image.open(io.BytesIO(map_bytes.content))
        img.show()
        
        zoom_level = input('zoom level: ')
        if int(zoom_level) <= 0:
            break
