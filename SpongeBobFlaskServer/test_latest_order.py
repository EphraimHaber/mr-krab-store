import json
import unittest
from main import app


class TestLatestOrder(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        app.config['latest_order'] = None

    def test_no_order_placed(self):
        response = self.app.get('/latest-order')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No order placed')

    def test_latest_order(self):
        expected_order = {'items': [
            {'description': 'The ultimate delicacy for the most adventurous eaters. Made from '
                            'the finest chum, this burger is a treat for the taste buds.',
             'id': 3, 'name': 'Chum Burger', 'price': 2.99, 'quantity': 3},
            {
                'description': 'A classic Krusty Krab side dish. Crunchy, salty, and a perfect complement to any '
                               'Krabby Patty.',
                'id': 4, 'name': 'Kelp Fries', 'price': 1.99, 'quantity': 2},
            {
                'description': "The star of the Krusty Krab's menu, this burger is a legend in Bikini Bottom. "
                               "Packed with fresh lettuce, tomatoes, onions, and the secret Krabby Patty sauce, "
                               "it's a must-try for anyone visiting the Krusty Krab.",
                'id': 1, 'name': 'Krabby Patty', 'price': 3.99, 'quantity': 2},
            {
                'description': "A delicious pizza made with fresh dough, sauce, and toppings, all cooked to "
                               "perfection in the Krusty Krab's oven. It's a hit with pizza lovers and SpongeBob "
                               "fans alike!",
                'id': 2, 'name': 'Krusty Krab Pizza', 'price': 5.99, 'quantity': 1}
        ]
        }

        app.config['latest_order'] = expected_order
        response = self.app.get('/latest-order')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, expected_order)

    def tearDown(self):
        app.config['latest_order'] = None


if __name__ == '__main__':
    unittest.main()
