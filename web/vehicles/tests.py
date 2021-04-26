from unittest.mock import Mock

import pytest
import requests
from django.urls import reverse

from vehicles.factories import CarFactory, CarRatingFactory
from vehicles.models import Car, CarRating


@pytest.mark.django_db
class TestCars:
    def setup_method(self, method):
        """ Create test data."""
        self.car1 = CarFactory()
        self.car2 = CarFactory()
        self.car3 = CarFactory()
        self.car4 = CarFactory()

        CarRatingFactory(car=self.car3, rating=3)
        CarRatingFactory(car=self.car3, rating=4)
        CarRatingFactory(car=self.car2, rating=1)

    def test_transactions_sum(self):
        assert self.car3.avg_rating == 3.5

    def test_cars_view_create_incorrect(self, client, mocker):
        mock_response = Mock()
        mocker.patch.object(requests, 'get', return_value=mock_response)
        mock_response.json.return_value = {'Results': []}
        mock_response.status_code = 200
        url = reverse('cars-list')
        response = client.post(url, {"model": "test", "make": "test"})
        assert response.status_code == 400
        assert response.json() == {'non_field_errors': ['Make with model does not exists']}
        assert Car.objects.count() == 4

    def test_cars_view_create_correct(self, client, mocker):
        mock_response = Mock()
        mocker.patch.object(requests, 'get', return_value=mock_response)
        mock_response.json.return_value = {'Results': [{'Model_Name': 'test'}]}
        mock_response.status_code = 200
        url = reverse('cars-list')
        response = client.post(url, {"model": "test", "make": "test"})
        print(response.json())
        assert response.status_code == 201
        assert Car.objects.count() == 5

    def test_cars_view_list(self, client):
        url = reverse('cars-list')
        response = client.get(url)
        assert response.status_code == 200
        assert response.json().get('count') == 4

    def test_cars_view_rate(self, client):
        url = reverse('cars-rate', kwargs={"pk": self.car1.pk})
        response = client.post(url, {"rating": 1}, content_type="application/json")
        assert response.status_code == 201
        assert CarRating.objects.count() == 4

    def test_cars_view_popular(self, client):
        url = reverse('cars-popular')
        response = client.get(url)
        assert response.status_code
        ids = [obj.get('id') for obj in response.json().get('results')]
        assert ids == [self.car3.id, self.car2.id, self.car1.id, self.car4.id]
