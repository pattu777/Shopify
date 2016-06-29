"""
Author - Chinmaya Kr. Patanaik
Email - patanaikchinmaya@gmail.com

Solution to Shopicruit task for fall internship position.

Third Party libraries used:
===========================
* requests
"""

import sys
import requests
import collections

computer_variants = {}
keyboard_variants = {}
URL = "http://shopicruit.myshopify.com/products.json"


def find_min_variants(computers, keyboards):
    """
    Returns the final list of products to buy.

    @params computers:   A sorted list of unique computer variant tuples.
    @paramas keyboards:  A sorted list of unique keyboard variant tuples.
    @type computers:     list
    @type keyboards:     list
    """
    total_weight = 0
    total_price = 0
    products = []

    if len(computers) <= len(keyboards):
        for item in computers:
            total_weight += item[1]['grams']
            total_price += item[1]['price']
            products.append(item)
        for index in xrange(len(computers)):
            total_weight += keyboards[index][1]['grams']
            total_price += keyboards[index][1]['price']
            products.append(keyboards[index])
    else:
        for item in keyboards:
            total_weight += item[1]['grams']
            total_price += item[1]['price']
            products.append(item)
        for index in xrange(len(keyboards)):
            total_weight += computers[index][1]['grams']
            total_price += computers[index][1]['price']
            products.append(computers[index])

    print "Total weight - %d" % total_weight
    print "Total price - %d" % total_price
    print "Products - %s" % products


def get_products():
    """
    Creates a HTTP request to get all the products in JSON format.
    And then generates a list of unique computers and keyboards and sorts them according to their prices.
    """
    response = requests.get(url=URL)
    if response.status_code != requests.codes.ok:
        print "Unable to send a request"
        return
    else:
        products = response.json()['products']
        for item in products:
            if item['product_type'] == 'Keyboard':
                for variant in item['variants']:
                    if variant['available']:

                        # Check if there's a previous entry with more price.
                        if variant['title'] in keyboard_variants:
                            if variant['title'] in keyboard_variants and variant['price'] < keyboard_variants[variant['title']]['price']:
                                keyboard_variants[variant['title']]['price'] = variant['price']
                                keyboard_variants[variant['title']]['grams'] = variant['grams']
                                keyboard_variants[variant['title']]['variant'] = variant
                        else:
                            keyboard_variants[variant['title']] = {'price' : float(variant['price']), 'grams' : variant['grams'], 'variant': variant}

            elif item['product_type'] == 'Computer':
                for variant in item['variants']:
                    if variant['available']:
                        if variant['title'] in computer_variants:

                            # Check if there's a previous entry with more price.
                            if float(variant['price']) < computer_variants[variant['title']]['price']:
                                computer_variants[variant['title']]['price'] = float(variant['price'])
                                computer_variants[variant['title']]['grams'] = variant['grams']
                                computer_variants[variant['title']]['variant'] = variant
                        else:
                            computer_variants[variant['title']] = {'price' : float(variant['price']), 'grams' : variant['grams'], 'variant': variant}


        # Sort the computers and keyboards according to their cost.
        computers = sorted(computer_variants.iteritems(), key=lambda (x, y): y['price'])
        keyboards = sorted(keyboard_variants.iteritems(), key=lambda (x, y): y['price'])
        find_min_variants(computers, keyboards)

if __name__ == '__main__':
    get_products()
    sys.exit(0)

