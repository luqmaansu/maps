from bs4 import BeautifulSoup
from .models import Location


def extract_opening_hours(item):
    """
    Helper function to extract opening hours from the HTML content of
    a single restaurant div of class .fp_listitem.

    It assumes that the opening hours are:
    1. Not the first <p> child -> that's the address
    2. Not an empty <p> element -> these are observed to be spacers
    3. Not the <p> with .infoboxlink -> these are map links

    These 3 rules are fleshed out as the CSS selector below.
    """

    opening_hours_selectors = (
        ".infoboxcontent > p:not(:first-child):not(:empty):not(.infoboxlink)"
    )
    opening_hours_elements = item.select(opening_hours_selectors)

    opening_hours = []
    for element in opening_hours_elements:
        opening_hours.append(element.text.strip())

    return opening_hours


def extract_restaurant_data(file_path="refs/website.html"):
    """
    The main function to extract restaurant data from the HTML file
    and returns a list of dictionaries.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

        soup = BeautifulSoup(html_content, "lxml")

        restaurants = []

        for item in soup.select(".fp_listitem:not([style*='display: none'])"):
            name = item.find("h4").text.strip()
            latitude = item.get("data-latitude")
            longitude = item.get("data-longitude")
            address = item.find("p").text.strip()
            opening_hours = extract_opening_hours(item)
            google_maps_url = item.find("a", href=True, target="_blank")["href"]
            waze_url = item.find_all("a", href=True, target="_blank")[1]["href"]

            restaurant_info = {
                "name": name,
                "address": address,
                "latitude": latitude,
                "longitude": longitude,
                "opening_hours": opening_hours,
                "google_maps_url": google_maps_url,
                "waze_url": waze_url,
            }

            restaurants.append(restaurant_info)

        return restaurants


def save_into_model(restaurants):
    """
    Helper function to save the restaurant restaurants into the Location model.

    Assumptions:
    1. `restaurants` is a list of dictionaries with the same keys as the
        Location model's field names.
    2. `name` field is unique for each restaurant. If the name already exists, it
        will update the existing record.
    """

    created_count, updated_count = 0, 0
    for restaurant in restaurants:
        location, created = Location.objects.update_or_create(
            name=restaurant["name"], defaults=restaurant
        )
        if created:
            created_count += 1
        else:
            updated_count += 1

    return created_count, updated_count
