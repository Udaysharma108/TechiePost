from django.core.management.base import BaseCommand
from bharatfeed.pipeline import IngestionPipeline

class Command(BaseCommand):
    """
    Custom management terminal engine to automate data sync cycles
    without needing manual interactive shell invocations.
    """
    help = 'Executes a single transactional sync cycle to ingest and filter live tech articles.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('[Pipeline] Initializing active ingestion cycle...'))
        
        try:
            # Instantiate our existing core execution engine
            pipeline = IngestionPipeline()
            synchronized_count = pipeline.run_sync_cycle()
            
            self.stdout.write(
                self.style.SUCCESS(f'[Pipeline] Database sync successful. Ingested {synchronized_count} records.')
            )
        except Exception as runtime_fault:
            self.stdout.write(
                self.style.ERROR(f'[Pipeline] Critical runtime operational failure: {str(runtime_fault)}')
            )