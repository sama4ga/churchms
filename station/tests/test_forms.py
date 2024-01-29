# import datetime
# from django.utils import timezone
# from django.test import SimpleTestCase
# from station.forms import StationForm

# class StationFormTest(SimpleTestCase):
#   def test_station_form_station_label(self):
#     form = StationForm()
#     self.assertTrue(form.fields['station'].label is None or form.fields['station'].label == 'station')

#   def test_station_form_date_created_too_far(self):
#     date = datetime.date.today() + datetime.timedelta(years=1000)
#     form = StationForm(data={"date_created":date})
#     self.assertFalse(form.is_valid())
