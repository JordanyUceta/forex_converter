from unittest import TestCase
from app import app
from flask import session

class FlaskTests(TestCase): 

    def test_index_form(self):
        with app.test_client() as client: 
            res = client.get('/')
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Currency Exchange!</h1>', html)

    def test_converter_form(self): 
        with app.test_client() as client: 
            res = client.get('/converter')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200) 
            self.assertIn('<form action="/posting" method="post">', html)

    def test_posting_form(self): 
        with app.test_client() as client: 
            res = client.post('/posting', data={'from': 'USD', 'to' : 'EUR', 'amount' : '10'})
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)

    def test_posting_redirection(self): 
        with app.test_client() as client: 
            res = client.post('/posting', data={'from': 'USD', 'to' : 'kkk', 'amount' : '10'})
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/converter')

    def test_posting_redirection_followed(self): 
        with app.test_client() as client: 
            res = client.post('/posting', data={'from': 'USD', 'to' : 'kkk', 'amount' : '10'}, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<form action="/posting" method="post">', html)