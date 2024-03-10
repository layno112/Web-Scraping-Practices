import csv
from bs4 import BeautifulSoup
import requests


path = "Book_infos.csv"


# Gets book data
def get_book_data():
    response = requests.get("https://books.toscrape.com/")
    soup = BeautifulSoup(response.content, "html.parser")

    books = []

    list_of_books = soup.find("ol", class_="row")

    # Runs through if the response is successful
    if response.status_code == 200:
        for book in list_of_books.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):

            book_details = {}
            book_link = book.find("h3").a["href"]

            if book_link:
                book_response = requests.get(f"https://books.toscrape.com/{book_link}")
                book_soup = BeautifulSoup(book_response.content, "html.parser")
                info = book_soup.find("div", class_="col-sm-6 product_main")
                columns = info.find_all(["h1", "p"])
                book_details["Name"] = columns[0].text
                book_details["Price"] = columns[1].text
                book_details["Stock"] = columns[2].text.strip()

                paragraph = book_soup.find("article", class_="product_page")
                description = paragraph.find_all("p")
                book_details["Description"] = description[3].text.strip()

                books.append(book_details)

    return books


def to_csv(books):
    with open(path, "w", newline='', encoding="utf-8-sig") as csv_file:
        columns = ["Name", "Price", "Stock", "Description"]
        csv_writer = csv.DictWriter(csv_file, fieldnames=columns)
        csv_writer.writeheader()
        for book in books:
            csv_writer.writerow(book)


book_data = get_book_data()
to_csv(book_data)



