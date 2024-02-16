import os
from django.test import TestCase
from .scraper import extract_restaurant_data, save_into_model
from .models import Location


class RefWebsiteExists(TestCase):
    def test_ref_website_exists(self):
        self.assertTrue(
            os.path.exists("refs/website.html"),
            "The file refs/website.html does not exist",
        )


class ScraperSanityTest(TestCase):
    """
    Sanity test with some simple examples from the website.html file.
    """

    def setUp(self):
        self.restaurants_dict = extract_restaurant_data()
        save_into_model(self.restaurants_dict)

    def test_extract_restaurant_data(self):
        self.assertEqual(
            self.restaurants_dict[0]["name"],
            "Subway Menara UOA Bangsar",
        )
        self.assertEqual(
            self.restaurants_dict[0]["address"],
            "Jalan Bangsar Utama 1, Unit 1-2-G, Menara UOA Bangsar, Kuala Lumpur, 59000",
        )
        self.assertEqual(
            self.restaurants_dict[0]["latitude"],
            "3.128099",
        )
        self.assertEqual(
            self.restaurants_dict[0]["longitude"],
            "101.678678",
        )
        self.assertEqual(
            self.restaurants_dict[0]["opening_hours"],
            ["Monday - Sunday, 8:00 AM - 8:00 PM"],
        )

    def test_simple_instance(self):

        instance = Location.objects.get(name="Subway Menara UOA Bangsar")

        self.assertEqual(
            instance.name,
            "Subway Menara UOA Bangsar",
        )
        self.assertEqual(
            instance.address,
            "Jalan Bangsar Utama 1, Unit 1-2-G, Menara UOA Bangsar, Kuala Lumpur, 59000",
        )
        self.assertEqual(
            instance.latitude,
            "3.128099",
        )
        self.assertEqual(
            instance.longitude,
            "101.678678",
        )
        self.assertEqual(
            instance.opening_hours,
            ["Monday - Sunday, 8:00 AM - 8:00 PM"],
        )
        self.assertEqual(
            instance.google_maps_url,
            "https://goo.gl/maps/8n6W5Syy3vUAGeQV8",
        )
        self.assertEqual(
            instance.waze_url,
            "https://www.waze.com/en/live-map/directions/my/federal-territory-of-kuala-lumpur/kuala-lumpur/subway-@-menara-uoa-bangsar?place=ChIJPWFRH5RJzDERvHvlO1uTQpY",
        )

    def test_instance_with_multiple_opening_hours(self):
        instance = Location.objects.get(name="Subway One Utama")

        self.assertEqual(
            instance.name,
            "Subway One Utama",
        )
        self.assertEqual(
            instance.address,
            "318A One Utama, Lower Ground Floor, New Wing, 1 Utama Shopping Centre, Petaling Jaya, 47800",
        )
        self.assertEqual(
            instance.latitude,
            "3.151251",
        )
        self.assertEqual(
            instance.longitude,
            "101.615116",
        )
        self.assertEqual(
            instance.opening_hours,
            [
                "0800 - 2200 (Sun - Thur)",
                "0800 - 2230 (Fri & Sat)",
            ],
        )

    def test_instance_with_closed_days(self):

        instance = Location.objects.get(name="Subway UOA Damansara")

        self.assertEqual(
            instance.name,
            "Subway UOA Damansara",
        )
        self.assertEqual(
            instance.address,
            "Unit 50-G-5, Ground Floor, Wisma UOA Damansara, No. 50, Jalan Dungun, Kuala Lumpur, 50490",
        )
        self.assertEqual(
            instance.latitude,
            "3.151729",
        )
        self.assertEqual(
            instance.longitude,
            "101.666006",
        )
        self.assertEqual(
            instance.opening_hours,
            [
                "Monday - Saturday, 8:00 AM – 8:30PM",
                "Sunday, Closed",
            ],
        )
