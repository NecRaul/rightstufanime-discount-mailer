import requests
import re
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import variables
import item_class
import mail

def url_check(url):
    pattern = "^https://www.rightstufanime.com/pl/.*$"
    return re.match(pattern, url) is not None
    
def process_url(url):
    # checking if the url is valid
    is_valid_url = url_check(url)
    
    # adding https:// to the start of the string if url is not valid
    url = f"https://{url}" if not is_valid_url else url
    
    # checking if the url is valid again
    is_valid_url = url_check(url)
    
    if (not is_valid_url):
        print("URL", url, "is not a rightstufanime public wishlist.")
        return None
    else:
        return url
        
def create_email_message(item_array):
    plain = ""
    html = "<html>\n\t<body>"
    for item in item_array:
        plain += f"{item.name} - ${item.price}:{item.link}\n"
        html += f"\n\t\t<p><a href=\"{item.link}\">{item.name}</a> - ${item.price}</p>"
    html += "\n\t</body>\n</html>"
    mail.send_check = True
    return [plain, html] # plain-text and HTML version of your message

if (mail.email_check and mail.password_check):
    # setting up mail attributes for later
    message = MIMEMultipart("alternative")
    message["Subject"] = variables.email_subject
    message["From"] = variables.sender_email
    message["To"] = variables.receiver_email
    
    for url in variables.urls:
        url = process_url(url) if process_url(url) else None
        if (url):
            r = requests.get(url)

            # parsing the content from the url with BeautifulSoup + lxml
            soup = BeautifulSoup(r.content, "lxml")

            # it only gets the first 12 items on the list
            # i get the number of pages (if it exists) to do more than 12
            page_numbers = soup.find_all("li", class_="global-views-pagination-links-number")

            if page_numbers != []:  # if the number of pages is more than 1
                for page_number in page_numbers:
                    r = requests.get(url + "?page=" + page_number.text)
                    soup = BeautifulSoup(r.content, "lxml")
                    item_array = item_class.find_discounted_item(soup)
            else:  # if the number of pages is 1
                item_array = item_class.find_discounted_item(soup)
                
            if len(item_array) != 0: # if any item in any url is on sale, it will send you mail
                message_parts = create_email_message(item_array)

                # turn these into plain/html MIMEText objects
                part1 = MIMEText(message_parts[0], "plain")
                part2 = MIMEText(message_parts[1], "html")

                # add HTML/plain-text parts to MIMEMultipart message
                # the email client will try to render the last part first
                message.attach(part1)
                message.attach(part2)

    if (mail.send_check):
        mail.send_mail(message.as_string())