import requests, re, json
from bs4 import BeautifulSoup


#########################
#extract urls function
def extract_urls(page_source):
    #set url function
    def get_url(soup, base_url='https://divar.ir'):
        a = soup.find('a')['href']
        if a.startswith('/'):
            a = base_url + a
        return a
    #bs4
    soup = BeautifulSoup(page_source, 'html.parser')
    #find all items
    result = soup.find_all('div', attrs={'class': 'post-card-item'})[1:-1]
    #set urls
    result = list(map(get_url, result))
    #out
    return result

#divar search
def divar_serach(query, city='tehran', catigory=None, limit = None):
    if catigory:
        url = f'https://divar.ir/s/{city}/{catigory}?q={query}'
    else:
        url = f'https://divar.ir/s/{city}?q={query}'
    ##
    try:
        response = requests.get(url)
    except:
        return
    #extract urls
    result = extract_urls(response.content)
    #set limit
    if limit:
        result = result[:limit]

    return result
#########################
def get_page_data_divar(url):
    try:
        response = requests.get(url)
    except:
        return
    ####
    data = {}
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.select('.kt-page-title__title')
    title = title[0].text if title else None
    info = soup.select('div.kt-base-row.kt-base-row--large')
    #info = soup.find_all('div',{'class':'kt-base-row'})
    for i in info:
        a = i.find('div',{'class':'kt-base-row__start'})
        b = i.find('div',{'class':'kt-base-row__end'})
        if (not b) or (not b):
            continue
        a, b = a.text , b.text
        if (not b) or (not b):
            continue
        data[a] = b
    info2 = soup.find_all('div',{'class':'kt-group-row-item--info-row'})
    for i in info2:
        a = i.find(attrs={'class':'kt-group-row-item__title'})
        b = i.find(attrs={'class':'kt-group-row-item__value'})
        if (not b) or (not b):
            continue
        a, b = a.text , b.text
        if (not b) or (not b):
            continue
        data[a] = b
    ####
    if not data:
        return
    description = soup.find('div',{'class':'kt-description-row'})
    description = description.text if description else None
    data = {
       'عنوان':title,
        **data,
       'توضیحات':description,
        'لینک':url,
    }
    ####
    return data



#extract cities
def Extract_cities():
    #send request
    try:
        response = requests.get('https://divar.ir')
    except:
        return []
    
    #extract cities
    soup = BeautifulSoup(response.content, "html.parser")
    cities = soup.find_all(name="div", attrs={'class':'city-group__button'})

    #extract city name
    def ex_city(city):
        a = city.find("a")['href']
        name = re.match(r'.*\/(.+)', a).group(1)
        return name
    
    #optimizing cities
    cities = list(map(ex_city, set(cities)))

    return cities


#json get cities
def Get_cities():
    return json.load(open("Cities.json","r"))

#json save cities
def Save_cities(cities):
    json.dump(cities, open("Cities.json","w"))
