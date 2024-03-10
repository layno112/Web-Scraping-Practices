import requests
from bs4 import BeautifulSoup
import csv


# Function to scrape the website
def scrape_books():
    url = "https://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    books = []

    for article in soup.find_all("article", class_="product_pod"):
        book = {}
        book["Name"] = article.h3.a["title"]
        book["Price"] = article.find("p", class_="price_color").text
        book["Stock"] = article.find("p", class_="instock availability").text.strip()

        # Accessing individual book page to get description
        book_url = url + article.h3.a["href"]
        book_response = requests.get(book_url)
        book_soup = BeautifulSoup(book_response.content, "html.parser")
        description_paragraphs = book_soup.find("article", class_="product_page").find_all("p")
        if len(description_paragraphs) >= 4:
            book["Description"] = description_paragraphs[3].text.strip()
        else:
            book["Description"] = "Description not available"

        books.append(book)

    return books


# Function to write data into CSV file
def write_to_csv(books):
    with open("books.csv", "w", newline="", encoding="utf-8-sig") as csvfile:
        fieldnames = ["Name", "Price", "Stock", "Description"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for book in books:
            writer.writerow(book)


# Main function
if __name__ == "__main__":
    books_data = scrape_books()
    write_to_csv(books_data)
    print("Scraping and writing to CSV file completed successfully.")