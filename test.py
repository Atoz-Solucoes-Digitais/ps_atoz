import unittest
import json

class TestProducts(unittest.TestCase):
    def test_prod(self):
        filename = "products.json"
        file = open(filename)
        products = json.loads(file.read())

        for product in products:
            self.assertEqual(type(product['name']), str)
            self.assertEqual(type(product['link']), str)
            self.assertEqual(type(product['image_link']), str)
            self.assertEqual(type(product['thermometer_rank']), int)
            self.assertEqual(type(product['recent_category_rank']), int)
            self.assertEqual(type(product['past_category_rank']), int)
            self.assertEqual(type(product['rank_percent_change']), int)
            self.average_rate(product)
            self.rate_qty(product)
            self.offers_qty(product)
            self.min_price(product)
            self.max_price(product)

        self.assertEqual(len(products), 50)
        file.close()

    def average_rate(self, product):
        if type(product['average_rate']) == float or type(product['average_rate']) == type(None):
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def rate_qty(self, product):
        if type(product['rate_qty']) == int or type(product['rate_qty']) == type(None):
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def offers_qty(self, product):
        if type(product['offers_qty']) == int or type(product['offers_qty']) == type(None):
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def min_price(self, product):
        if type(product['min_price']) == float or type(product['min_price']) == type(None):
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def max_price(self, product):
        if type(product['max_price']) == float or type(product['max_price']) == type(None):
            self.assertTrue(True)
        else:
            self.assertTrue(False)
        

if __name__ == '__main__':
    unittest.main()