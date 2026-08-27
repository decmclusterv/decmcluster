from django.core.management.base import BaseCommand

from cluster_contact.services.import_service import import_contacts_from_docx_file


class Command(BaseCommand):
    help = "Imports contacts from DECM Cluster Mailing List docx file into ClusterContact table."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            help="Optional path to custom docx file",
        )

    def handle(self, *args, **options):
        file_path = options.get("file")
        self.stdout.write(self.style.NOTICE("Starting cluster contact import..."))
        result = import_contacts_from_docx_file(file_source=file_path)
        self.stdout.write(
            self.style.SUCCESS(
                f"Import completed! Total: {result['total_processed']} | "
                f"Created: {result['created_count']} | Updated: {result['updated_count']}"
            )
        )
