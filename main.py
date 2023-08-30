import requests
import re
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import variables
import item_class
import mail

mail_boolean = False
url_number = 0

def url_check(url):
    pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
    return re.match(pattern, url) is not None

def mail_check(mail):
    pattern = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\\.[A-Z|a-z]{2,})+"
    return re.match(pattern, mail) is not None

sender_boolean = mail_check(variables.sender_email)
receiver_boolean = mail_check(variables.receiver_email)
        
if not sender_boolean and not receiver_boolean:
    print("Sender email and receiver email is incorrect.")
elif not sender_boolean:
    print("Sender email is incorrect.")
elif not receiver_boolean:
    print("Receiver email is incorrect.")
else:
    # provide a link(s) starting with http/https
    # requests doesn't recognize it otherwise
    for url in variables.urls:
        # checking if the url is valid
        is_valid_url = url_check(url)
        
        # adding https:// to the start of the string if url is not valid
        url = f"https://{url}" if not is_valid_url else url
        
        # checking if the url is valid again
        is_valid_url = url_check(url)
        
        if (not is_valid_url):
            url_number += 1
            print("URL ", url_number, " is incorrect.")
        else:
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
                    item_array = item_class.FindDiscountedItem(soup)
            else:  # if the number of pages is 1
                item_array = item_class.FindDiscountedItem(soup)
                
            if len(item_array) != 0:
                mail_boolean = True # if any item in any url is on sale, it will send you mail
                message = MIMEMultipart("alternative")
                message["Subject"] = variables.email_subject
                message["From"] = variables.sender_email
                message["To"] = variables.receiver_email

                # create the plain-text and HTML version of your message
                plain = ""
                html_start = "<html>\n\t<body>"
                html_body = ""
                html_end = "\n\t</body>\n</html>"

                for item in item_array:
                    plain = plain + item.name + " - $" + str(item.price) + ":" + item.link + "\n"
                    html_body = (
                        html_body
                        + '\n\t\t<p><a href="'
                        + item.link
                        + '">'
                        + item.name
                        + "</a> - $"
                        + str(item.price)
                        + "</p>"
                    )

                html = html_start + html_body + html_end

                # turn these into plain/html MIMEText objects
                part1 = MIMEText(plain, "plain")
                part2 = MIMEText(html, "html")

                # add HTML/plain-text parts to MIMEMultipart message
                # the email client will try to render the last part first
                message.attach(part1)
                message.attach(part2)

    if (mail_boolean):
        mail.SendMail(message.as_string())