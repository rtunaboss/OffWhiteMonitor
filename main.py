from bs4 import BeautifulSoup as bs
import requests
import time
import itertools

'''
TODO:
Add proxy support
Add threading support
Add search for different localles

'''

headers = {
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
}

keywords = [
    "UNC",
    "Menta",
    "Jordan",
    "force",
    #"blue+diagonals+raincoat", 
    
    #TODO Add more keywords
]

def monitor_website(url, keywords):
    #looking for products available from an URL

    #making a request to the url
    try:
        r = requests.get(url, headers=headers)
    except Exception as e:
        print(e)

    #parsing the page
    page = bs(r.text, "html.parser")

    #looking for all the products on the webpage
    html_product_list = page.find_all("article", class_="product")

    #geting the name of a product, its price and its link 
    for product_html in html_product_list:
        for keyword in keywords:
            #remove whitespace from a keyword
            keyword = keyword.strip()

            #check if any of keywords are in the sourcecode of each product
            if keyword in product_html:
                
                #find and generate a product link
                html_product = product_html.find("a", itemprop="url")
                href = html_product["href"]
                product_link = "https://www.off---white.com" + href
                
                #find price of the product
                price = html_product.find("span", itemprop="price")["content"]

                #find the name of the products
                name = html_product.find("div", class_="brand-name").text.strip()

                #find the image of the product
                #img = product_html.find("img", itemprop="image")["src"]

                print(f"\nFound {name} for {price}. \nAvailable from:\t {product_link}")
                

def monitor_search(keywords):
    #search OW website for keywords

    for keyword in keywords:

        #make sure keywords are lowercase
        keyword = keyword.lower()

        #creates an url for a search
        url = "https://www.off---white.com/en/GB/search?q=" + keyword
        
        #make a search request for the keyword and parse it
        r = requests.get(url, headers=headers)
        page = bs(r.text, "html.parser")

        #find all products that have been found in search
        products = page.find_all("article", class_="product")
        if products == []:
            continue

        for product in products:

            #generate product link
            html_product = product.find("a", itemprop="url")
            href = html_product["href"]
            product_link = "https://www.off---white.com" + href + "#"

            #find name of the product
            name = product.find("div", class_="brand-name").text.strip()
            
            #find price of the product
            price = product.find("span", itemprop="price")["content"]
            
            #check if product is in stock
            soldout = product.find("div", class_="availability not_on_sale")
            if soldout == None:
                print(f"FOUND: {name}, for {price}, \navailable from:\t{product_link}")
            else:
                print(f"Product {name} is out of stock...")
                continue


#load sites
websites = open("pages.txt", "r")

#start monitoring with an infinite loop
while(True):
    for website in itertools.cycle(websites):

        print("Monitoring...")
        monitor_website(website, keywords)
        monitor_search(keywords)

        #delay to prevent getting your IP banned
        print("Sleeping for 3s...")
        time.sleep(3)