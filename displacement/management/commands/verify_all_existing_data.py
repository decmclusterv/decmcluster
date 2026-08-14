from django.core.management.base import BaseCommand
from displacement.models import Displacement
from evacuation_centre.models import EvacuationCentre
from fivew.models import FiveWActivity
from village_assessment.models import VillageAssessment


class Command(BaseCommand):
    help = "Verifies all existing unverified data for Displacement, EvacuationCentre, FiveWActivity, and VillageAssessment"

    def handle(self, *args, **options):
        # 1. Displacement
        self.stdout.write("Processing Displacement...")
        unverified_displacement = Displacement.objects.filter(
            status=Displacement.StatusChoices.UNVERIFIED
        )
        disp_count = unverified_displacement.count()
        if disp_count > 0:
            self.stdout.write(f"Updating {disp_count} Displacement records to verified...")
            unverified_displacement.update(status=Displacement.StatusChoices.VERIFIED)
            self.stdout.write(self.style.SUCCESS(f"Successfully verified {disp_count} Displacement records."))
        else:
            self.stdout.write(self.style.WARNING("No unverified Displacement records found."))

        # 2. Evacuation Centre
        self.stdout.write("\nProcessing Evacuation Centre...")
        unverified_ec = EvacuationCentre.objects.filter(
            status=EvacuationCentre.StatusChoices.UNVERIFIED
        )
        ec_count = unverified_ec.count()
        if ec_count > 0:
            self.stdout.write(f"Updating {ec_count} Evacuation Centre records to verified...")
            unverified_ec.update(status=EvacuationCentre.StatusChoices.VERIFIED)
            self.stdout.write(self.style.SUCCESS(f"Successfully verified {ec_count} Evacuation Centre records."))
        else:
            self.stdout.write(self.style.WARNING("No unverified Evacuation Centre records found."))

        # 3. 5W Activity
        self.stdout.write("\nProcessing 5W Activity...")
        unverified_fivew = FiveWActivity.objects.filter(
            status=FiveWActivity.StatusChoices.UNVERIFIED
        )
        fivew_count = unverified_fivew.count()
        if fivew_count > 0:
            self.stdout.write(f"Updating {fivew_count} 5W Activity records to verified...")
            unverified_fivew.update(status=FiveWActivity.StatusChoices.VERIFIED)
            self.stdout.write(self.style.SUCCESS(f"Successfully verified {fivew_count} 5W Activity records."))
        else:
            self.stdout.write(self.style.WARNING("No unverified 5W Activity records found."))

        # 4. Village Assessment
        self.stdout.write("\nProcessing Village Assessment...")
        unverified_village = VillageAssessment.objects.filter(
            status=VillageAssessment.StatusChoices.UNVERIFIED
        )
        village_count = unverified_village.count()
        if village_count > 0:
            self.stdout.write(f"Updating {village_count} Village Assessment records to verified...")
            unverified_village.update(status=VillageAssessment.StatusChoices.VERIFIED)
            self.stdout.write(self.style.SUCCESS(f"Successfully verified {village_count} Village Assessment records."))
        else:
            self.stdout.write(self.style.WARNING("No unverified Village Assessment records found."))

        self.stdout.write(self.style.SUCCESS("\nAll model verification processing completed successfully."))
