import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import variables
import item_class
import mail

mail_check = False

# provide a link(s) starting with http/https
# requests doesn't recognize it otherwise
for website in variables.websites:
    r = requests.get(website)

    # parse the content from the website with BeautifulSoup + lxml
    # you can also use html.parser but lxml is more comfortable for me
    soup = BeautifulSoup(r.content, "lxml")

    # it can't do more than 12 at a time so we need the number of pages
    page_numbers = soup.find_all("li", class_="global-views-pagination-links-number")

    if page_numbers != []:  # if the number of pages is more than 1, code below will execute
        for page_number in page_numbers:
            r = requests.get(website + "?page=" + page_number.text)
            soup = BeautifulSoup(r.content, "lxml")
            item_array = item_class.FindDiscountedItem(soup)

    else:  # if the number of pages is 1, code below will execute
        item_array = item_class.FindDiscountedItem(soup)
        
    if len(item_array) != 0: # if any item is on sale, it will send you mail
        mail_check = True
        message = MIMEMultipart("alternative")
        message["Subject"] = variables.email_subject
        message["From"] = variables.sender_email
        message["To"] = variables.receiver_email

        # Create the plain-text and HTML version of your message
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

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(plain, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

if (mail_check):
    mail.SendMail(message.as_string())