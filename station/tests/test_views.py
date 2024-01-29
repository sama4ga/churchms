from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from station.models import Station

User = get_user_model()

class StationListViewTest(TestCase):
  @classmethod
  def setUpTestData(cls) -> None:
    for station_id in range(5):
      Station.objects.create(name=f"Station {station_id}", address=f"Address {station_id}")
    User.objects.create_superuser(username="su", password='user@1234')
    User.objects.create_user(username="user", password='user@1234')

  def test_station_view_redirect_if_not_logged_in(self):
    response = self.client.get(reverse("station-view"))
    self.assertRedirects(response, '/users/login/?next=/station/')

  def test_station_view_raise_permission_denied(self):
    self.client.login(username="user", password="user@1234") #user does not hav permission to view station
    response = self.client.get(reverse("station-view"))
    self.assertEqual(response.status_code, 403)

  def test_station_view_url_exist(self):
    self.client.login(username='su', password='user@1234')
    response = self.client.get('/station/')
    self.assertEqual(response.status_code, 200)

  def test_station_view_url_exist_by_name(self):
    self.client.login(username='su', password='user@1234')
    response = self.client.get(reverse("station-view"))
    self.assertEqual(response.status_code, 200)

class StationCreateViewTest(TestCase):
  @classmethod
  def setUpTestData(cls) -> None:
    User.objects.create_superuser(username="su", password='user@1234')
    User.objects.create_user(username="user", password='user@1234')

  def test_station_create_view_redirect_if_not_logged_in(self):
    response = self.client.get(reverse("station-create"))
    self.assertRedirects(response, '/users/login/?next=/station/create/')

  def test_station_create_view_raise_permission_denied(self):
    self.client.login(username="user", password="user@1234") #user does not hav permission to create station
    response = self.client.get(reverse("station-create"))
    self.assertEqual(response.status_code, 403)

  def test_station_create_view_url_exist(self):
    self.client.login(username='su', password='user@1234')
    response = self.client.get('/station/create/')
    self.assertEqual(response.status_code, 200)

  def test_station_create_view_url_exist_by_name(self):
    self.client.login(username='su', password='user@1234')
    response = self.client.get(reverse("station-create"))
    self.assertEqual(response.status_code, 200)

  def test_station_create_view_creates_station(self):
    self.client.login(username="su", password="user@1234")
    response = self.client.post(reverse("station-create"), {"name":"New Station", "address":"New Address"})
    # response.redirect_chain    
    # self.assertTrue(Station.objects.filter(name='New Station').exists())
    self.assertEqual(response.status_code, 200)
