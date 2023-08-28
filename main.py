from bs4 import BeautifulSoup
import requests
import variables

# provide a link starting with http/https
# requests doesn't recognize it otherwise
r = requests.get(variables.website)

# parse the content from the website with BeautifulSoup + lxml
# you can also use html.parser but lxml is more comfortable for me
soup = BeautifulSoup(r.content, "lxml")

# it can't do more than 12 at a time so we need the number of pages
page_numbers = soup.find_all("li", class_="global-views-pagination-links-number")

if page_numbers != []:  # if the number of pages is more than 1, code below will execute
    for page_number in page_numbers:
        r = requests.get(variables.website + "?page=" + page_number.text)
        soup = BeautifulSoup(r.content, "lxml")
        item_array = []

else:  # if the number of pages is 1, code below will execute
    item_array = []