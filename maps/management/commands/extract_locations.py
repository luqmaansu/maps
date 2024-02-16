from django.core.management.base import BaseCommand
from maps.models import Location
from maps.scraper import extract_restaurant_data, save_into_model


class Command(BaseCommand):
    help = "Extracts restaurant data from the website.html file and saves it into the Location model."

    def handle(self, *args, **options):
        restaurants_dict = extract_restaurant_data()

        # Display confirmation prompt
        self.stdout.write(f"New locations to be created: {len(restaurants_dict)}")
        confirm = input("Do you want to proceed? [y/N] ")

        # Proceed based on user input
        if confirm.lower() == "y":
            created_count, updated_count = save_into_model(restaurants_dict)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created {created_count} and updated {updated_count} locations."
                )
            )
        else:
            self.stdout.write(self.style.WARNING("Operation aborted by the user."))
