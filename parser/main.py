import requests
from bs4 import BeautifulSoup
from db.database import manager

from multiprocessing import Pool
from datetime import datetime

manager = manager

def get_html(URL): 
    # Делать запрос по ссылке и возвращать html код этой страницы
    response = requests.get(URL)
    return response.text


def get_posts_links(html):
    links = []
    soup = BeautifulSoup(html, "html.parser")
    table_data = soup.find("div", {"class":"search-results-table"})
    data = table_data.find("div", {"class":"table-view-list"})
    posts = data.find_all("div", {"class":"list-item"})
    for p in posts:
        href=p.find("a").get("href")
        full_url = "https://www.mashina.kg"+href
        links.append(full_url)
    return links # возвращает ссылки на детальную страницу постов

def get_detail_post(html, post_url):
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", {"class":"details-wrapper"})
    detail = content.find("div",{"class":"details-content"})
    title = detail.find("div", {"head-left"}).find("h1").text
    som = detail.find("div", {"class":"sep main"}).find("div",{"class":"price-som"}).text
    dollar = detail.find("div", {"class":"sep main"}).find("div",{"class":"price-dollar"}).text
    add_price = detail.find("div",{"class":"sep addit"}).find_all("div")
    tenge = add_price[1].text
    ruble = add_price[0].text
    mobile = detail.find("div",{"class":"details-phone-wrap"})
    mobile = mobile.find("div",{"class":"number"}).text
    description = detail.find("h2", {"class":"comment"}).text
    som = int(som.replace("сом", "").strip().replace(" ", ""))
    dollar = int(dollar.replace("$", "").strip().replace(" ", ""))
    data = {
        "title":title,
        "som":som,
        "dollar":dollar,
        "mobile":mobile,
        "description":description,
        "link":post_url
    }
    return data

def get_lp_number(html):
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", {"class":"search-results-table"})
    ul = content.find("ul", {"class":"pagination"})
    lp = ul.find_all("a", {"class":"page-link"})[-1]
    n=lp.get("data-page")
    return int(n)

def write_data(data): # Запись в базу
    result = manager.insert_car(data)
    return result

def get_parse_page(page):
    URL_MAIN = "https://www.mashina.kg/search/all/all/"
    filter = "?currency=2&price_to=10000&region=1&sort_by=upped_at+desc&steering_wheel=1&town=2"
    FULL_URL = URL_MAIN + filter
    print(f"Парсинг страницы:{page}")
    FULL_URL += f"&page={page}"
    html = get_html(FULL_URL)
    post_links = get_posts_links(html)
    for link in post_links:
        if not manager.check_car_in_db(link):
            post_html = get_html(link)
            post_data = get_detail_post(post_html, post_url=link)
            write_data(data=post_data)

def main():
    start = datetime.now()
    passed_posts=0
    URL_MAIN = "https://www.mashina.kg/search/all/all/"
    filter = "?currency=2&price_to=10000&region=1&sort_by=upped_at+desc&steering_wheel=1&town=2"
    FULL_URL = URL_MAIN + filter
    last_page = get_lp_number(get_html(FULL_URL))
    with Pool(40) as p:
        p.map(get_parse_page, range(1, 10+1))
    
    end = datetime.now()
    print("Время выполнения: ", end-start)
    print("Количество постов , которые были пропущены: ", passed_posts)

if __name__=="__main__":
    manager.create_table()
    main()