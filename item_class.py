import variables

class Item:
    def __init__(self, name, price, link):
        self.name = name
        self.price = price
        self.link = "https://www.rightstufanime.com" + link


# item array to contain items that we consider discounted
item_array = []


def FindDiscountedItem(
    soup,
):
    # information about the twelve items in the current page
    items_content = soup.find_all(
        "div", class_="facets-items-collection-view-cell-span3"
    )
    for item_content in items_content:
        # get each items' price
        price_str = item_content.find(
            "span", class_="product-views-price-lead", itemprop="price"
        ).text

        # convert it to float
        price = float(price_str)
        if price < variables.base_price:
            name = item_content.find("span", class_="facets-item-cell-grid-name").text
            link = item_content.find(
                "a", class_="facets-item-cell-grid-link-image"
            ).get("href")
            item = Item(name, price, link)
            item_array.append(item)
    return item_array
