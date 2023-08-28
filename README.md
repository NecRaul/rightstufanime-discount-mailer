# RightStufAnime-Discount-Mailer

Mails you if anything on your public wishlist is on discount.

## Requirements

`requests` is used to get the website content.

`BeautifulSoup` is used to parse the content with specified values and get the important information.

You can install these packages by running

```Python
pip install -r requirements.txt
```

Python's native `email`, `smtplib` and `ssl` packages are used to send mail once all the important information has been acquired.

## How it works

You have to have a public wishlist with more than 1 item in it. Each time you run the script, it will check all the items on your wishlist, compare it to the price you have specified, if any of them have gone below the specified price, you'll recieve an email.
