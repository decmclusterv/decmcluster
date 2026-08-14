from django.core.management.base import BaseCommand
from displacement.models import Displacement


class Command(BaseCommand):
    help = "Verifies all existing unverified displacement records"

    def handle(self, *args, **options):
        self.stdout.write("Finding unverified displacements...")
        unverified_qs = Displacement.objects.filter(
            status=Displacement.StatusChoices.UNVERIFIED
        )
        count = unverified_qs.count()
        if count == 0:
            self.stdout.write(
                self.style.SUCCESS("No unverified displacement records found.")
            )
            return

        self.stdout.write(f"Updating {count} records to verified status...")
        updated_count = unverified_qs.update(
            status=Displacement.StatusChoices.VERIFIED
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully verified {updated_count} existing displacement records."
            )
        )
