from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class BoggleTestCase(TestCase):
    # TODO -- write tests for every view function / feature!
    def setUp(self):
        """TODO before each test."""
        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_homepage(self):
        """Make sure HTML is shown and info is in session."""
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<p id="title"><em>Boggle!</em></p>', html)
            self.assertIsNone(session.get('num_plays'))
            self.assertIn(b'Seconds Left:', response.data)
            
    def test_word_on_board(self):
        """Test if word is on the board (with board in test case)."""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["M", "O", "U", "S", "E"], 
                                 ["M", "O", "U", "S", "E"], 
                                 ["M", "O", "U", "S", "E"], 
                                 ["M", "O", "U", "S", "E"], 
                                 ["M", "O", "U", "S", "E"]]
        response = self.client.get('/check-word?word=mouse')
        self.assertEqual(response.json['result'], 'ok')        

    def test_word_not_on_board(self): 
        """Test if word is in dictionary."""

        self.client.get('/')
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.json['result'], 'not-on-board')
    
    def test_not_word(self):
        """Test if word is real word."""

        self.client.get('/')
        response = self.client.get('/check-word?word=phlagel')
        self.assertEqual(response.json['result'], 'not-word')
    
        
            
            
    