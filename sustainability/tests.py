from django.test import TestCase, Client
from django.urls import reverse
from .models import UserScore, SearchHistory
from django.contrib.auth.models import User
from .utils import get_eco_alternatives
import os
from unittest.mock import patch

class EcoSwapTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_index_page_loads(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertNotEqual(response.status_code, 200) # Should redirect to login
        
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    @patch('sustainability.utils.get_eco_alternatives')
    def test_search_creates_history_and_points(self, mock_get_eco):
        # Mock API response
        mock_get_eco.return_value = [{'name': 'Bamboo', 'impact_score': 10, 'link': 'http://test.com'}]
        
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('index'), {'product_name': 'Plastic'})
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(SearchHistory.objects.filter(query='Plastic').exists())
        self.assertTrue(UserScore.objects.filter(user=self.user).exists())
        self.assertEqual(UserScore.objects.get(user=self.user).points, 10)

    def test_gemini_api_call_structure(self):
         # Integration test logic
         pass
