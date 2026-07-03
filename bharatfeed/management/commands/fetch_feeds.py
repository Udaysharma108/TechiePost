from django.core.management.base import BaseCommand
from bharatfeed.pipeline import IngestionPipeline


from django.core.management.base import BaseCommand
from bharatfeed.pipeline import IngestionPipeline

class Command(BaseCommand):
    help = "Triggers the dual-stream engineering ingestion and NLP pipeline arrays."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("[Pipeline] Launching active pipeline execution layer..."))
        pipeline = IngestionPipeline()
        records = pipeline.run_sync_cycle()
        self.stdout.write(self.style.SUCCESS(f"[Pipeline] Execution success. Database tables populated with {records} updates."))
