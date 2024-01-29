from django.test import TestCase
from station.models import Station

class StationModelTest(TestCase):

  @classmethod
  def setUpTestData(cls) -> None:
    Station.objects.create(name="Station1", address="Address1")

  def test_get_absolute_url(self):
    station = Station.objects.get(id=1)
    self.assertEqual(station.get_absolute_url(), "/station/")

  def test_date_created_label(self):
    station = Station.objects.first()
    field_label = station._meta.get_field("date_created").verbose_name
    self.assertEqual(field_label, "date created")

  def test_object_name_is_name_space_station(self):
    station = Station.objects.first()
    expected_object_name = f"{station.name} station"
    self.assertEqual(str(station), expected_object_name)
