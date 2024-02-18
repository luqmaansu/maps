# Summary

This web application is developed using Django to visualize the locations of Subway restaurants in Kuala Lumpur, Malaysia. The data used was initially scraped from Subway Malaysia's website on 16th February 2024. The web app was developed using the followings, among others:

1. Python 3.11.5
2. Django 5.0.2
3. Leaflet 1.9.4
4. Bootstrap 5.3.2

# For end users
1. The web application can be accessed at `luqmaans.pythonanywhere.com`

# For developers
### Important setup notes
1. This project uses `local_settings.py` to store secrets. Make sure it is present within `_project\` directory i.e., where `settings.py` is located.
2. Run `python manage.py extract_locations` to populate the `Location` model with data scraped from the reference website.
3. Only after executing `extract_locations`, then run `python manage.py generate_distance` to populate the `Distance` model with data calculated from the `Location` instances.


### Website scraping
The website was scraped by visiting `https://subway.com.my/find-a-subway`, entering "Kuala Lumpur" in the search bar, and copying the relevant sections of the results. The relevant part was determined to be within the `div` element with id `id="fp_locationlist"`, which is then copied, pasted, and saved as `refs\website.html`.

### Database storage
There are 2 models involved in this application, `Location` and `Distance`. Note that this project does not use Django's built in GIS functionality, which would have been the ideal setup for a geographical application such as this. The simple reason is due to technical difficulties in setting up the pre-requisites (perhaps on Windows), so an alternative of using the basic Django functionality was chosen to just proceed with this task.

This relates to why `Distance` is stored as a database table instead of using GIS DB operations. Indeed this causes a lot of `Distance` instance to be required due to the O(n<sup>2</sup>) relationship (137 locations results in 9,000+ distances), but it might be a reasonable trade-off considering that the locations are not going to be updated too frequently, and instead, the distances are queried a lot.

### Geocoding and API development
The geographical coordinates for each location alongside other attributes can be retrieved via a GET API request at `api/locations/`. It accepts an optional query parameter `range`, e.g., `api/locations/?range=5` which will also return nearby locations with the given value in km, queried on `Distance`.

### Query search box
The single search bar is a simple `icontains` search on 4 fields: "name", "address", "latitude", and "longitude" and returns all instances that match any one of the fields.

### Priority improvements
If more time and resource was available, the following is a list of proposed improvements that can be done, listed in priority:

1. Search box functionality to process natural-language-like queries as per requirement.
2. Use Django's GIS package properly
3. Use GIS DB calculations to retrieve nearby locations within the specified range