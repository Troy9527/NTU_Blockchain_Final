import os, csv, bs4, re, sys, io
import urllib.request


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
    
    find = 0
    f = io.StringIO(text)
    for line in f:
        if "];" in line:
            find = 0

        if find == 1:
            temp = re.sub(r"^[\t\s]+", "", line)
            temp = re.sub(r"[\t\s]+$", "", temp)
            temp = temp.split(",", 1)
            temp = "(" + temp[0][6:] + "," + temp[1][6:-1].strip('}') + ")"
            
            ret += temp + ","

        if "loc_arr[" in line and "] = [" in line:
            find = 1

    ret = ret[:-1]
    if not ret:
        ret = "None"
    return ret

if __name__=='__main__':

    logno = sys.argv[1]

    html_bytes = urllib.request.urlopen('https://fc.efoodex.net/portal.php?oid=' + str(logno) + '&m=1').read()
    html_decode = html_bytes.decode('utf-8')


    soup = bs4.BeautifulSoup(html_decode, "lxml")

    oid = logno


    # remove prefix and training whitespaces
    product_name = soup.find_all("meta")[6]["content"]
    print("產品名稱: " + str(product_name))
    
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

    print("產出組織: " + str(organization))
    print("產出日期: " + str(produce_date))
    print("有效日期: " + str(expired_date))
    print("產出組織: " + str(produce_amount))
    print("剩餘數量: " + str(remaining))

    # parsing transaction
    transac = soup.body.find_all('a', class_='btn btn-dark btn-lg btn-width')
    num = len(transac)
    transac_str = parsing_transac(transac)

    print("作業數量: " + str(num))
    print("作業過程: " + str(transac_str))

    # parsing GPS
    GPS = parsing_GPS(html_decode)

    print("GPS: " + str(GPS))
