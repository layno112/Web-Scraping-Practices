import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BS
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import csv

url = "https://www.reddit.com/r/gaming/"

options = webdriver.ChromeOptions()
options.page_load_strategy = "normal"
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
driver.implicitly_wait(10)

num_of_posts = 0

def main():
    links = get_reddit_post_links(url)
    posts = get_reddit_post_data(links)

    csv_name = "Reddit_posts.csv"
    to_csv(posts, "utf-8", csv_name)


def to_csv(posts, encoding, csv_name):
    with open(csv_name, "w", encoding=encoding) as csv_file:
        columns = ["Title", "Text", "Links"]
        csv_writer = csv.DictWriter(csv_file, fieldnames=columns)
        csv_writer.writeheader()
        for post in posts:
            csv_writer.writerow(post)
    driver.quit()


# Gets reddit post links
def get_reddit_post_links(source, num=3):
    driver.get(source)

    links = []

    main = driver.find_element(by=By.ID, value="main-content")

    # Gets the first 3 post links
    for article in main.find_elements(by=By.TAG_NAME, value="article"):
        article_element = article.get_attribute("outerHTML")
        article_element = BS(article_element, "lxml")
        post_link = article_element.find("a")["href"]
        links.append(post_link)

    # Gets the post links under the faceplate-batch.
    for faceplate in driver.find_elements(by=By.TAG_NAME, value="faceplate-batch"):
        articles = faceplate.find_elements(by=By.TAG_NAME, value="article")
        for article in articles:
            article_element = article.get_attribute("outerHTML")
            article_element = BS(article_element, "lxml")
            post_link = article_element.find("a")["href"]
            links.append(post_link)

    return links[:num]


# Gets reddit post data
def get_reddit_post_data(posts):
    list_of_posts = []

    for link in posts:
        post = {}

        try:
            driver.get(f"https://www.reddit.com{link}")
            title = driver.find_element(by=By.XPATH, value="//h1[contains(@id, 'post-title')]")
            title = title.text
            post["Title"] = title
            p_tags = driver.find_element(by=By.XPATH, value="//div[contains(@id, 't3')]")
            p_tags = p_tags.find_elements(by=By.TAG_NAME, value="p")
            print(len(p_tags))
            text = ""
            for paragraph in p_tags:
                text = text + paragraph.text
            post["Text"] = text
            post["Links"] = f"https://www.reddit.com{link}"

        except NoSuchElementException:
            post["Text"] = "None"

        list_of_posts.append(post)
    return list_of_posts


if __name__ == '__main__':
    main()
