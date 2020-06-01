import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from pyecharts import Bar
import seaborn as sns
all_data = []      # an empty list used later to hold data.


def parse_page(url):    # method for getting the information from the website

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
    response = requests.get(url,headers = header) # use the requests.get method to get the full text.
    text = response.content.decode('utf-8')   # change the text format to be readable
    soup = BeautifulSoup(text, 'html5lib')
    data= soup.find('div',class_='conMidtab')   # use find method to find the block of code we are looking for
    tables = data.find_all('table')               # use find_all method to find tables in each of the block
    # print(len(tables))
    if url == 'http://www.weather.com.cn/textFC/hb.shtml':     # since each sub-page's structure is a
        for table in tables:                                    # little bit different , we need to use different
            trs = table.find_all('tr')[2:]                      # strategies to parse them
            for tr in trs:
                tds=tr.find_all('td')
                city_td=tds[0]
                city= list(city_td.stripped_strings)[0]     # find the city name
                temp_td= tds[-2]
                min_temp = list(temp_td.stripped_strings)[0]    # find the minimum temperature
                all_data.append({'city':city,'min_temp': int(min_temp)})    # format them as dic and stored in the list
    else:
        for table in tables:
            trs = table.find_all('tr')[2:]
            for index, tr in enumerate(trs):
                tds=tr.find_all('td')
                city_td = tds[0]
                if index == 0:
                    city_td=tds[1]
                city= list(city_td.stripped_strings)[0]
                temp_td= tds[-2]
                min_temp = list(temp_td.stripped_strings)[0]
                all_data.append({'city':city,'min_temp': int(min_temp)})


def main():
    # a list contains all the urls for the weather in different cities
    url = ['http://www.weather.com.cn/textFC/hb.shtml','http://www.weather.com.cn/textFC/db.shtml',
            'http://www.weather.com.cn/textFC/hd.shtml','http://www.weather.com.cn/textFC/gat.shtml',
           'http://www.weather.com.cn/textFC/hz.shtml','http://www.weather.com.cn/textFC/hn.shtml',
           'http://www.weather.com.cn/textFC/xb.shtml','http://www.weather.com.cn/textFC/xn.shtml']

    # loop through every urls
    for i in url:
        parse_page(i)
        # sort the list according to the min temperature
    all_data.sort(key=lambda x: x['min_temp'])
    # use the first 10 data
    data = all_data[0:10]
    # get the 10 lowest temperature's city name
    city=list(map(lambda x: x['city'], data))
    # get the corresponding min temperature
    min_temp = list(map(lambda x: x['min_temp'], data))
    # print(city)   code to check whether we obtain the results correct
    # print(min_temp)
    chart = Bar('The lowest weather in China')      # using bar chart to display the results
    chart.add('', city,min_temp)
    chart.render('ranking.html')                # save the data visualization within the html file.
    # sns.barplot(x=city,y=min_temp)
    # plt.show()
    # # url = 'http://www.weather.com.cn/textFC/gat.shtml'
    # parse_page(url)


if __name__=='__main__':
    main()