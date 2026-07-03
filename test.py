import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
try:
    django.setup()
except Exception as setup_error:
    print(f"Framework runtime setup failed: {setup_error}")
    sys.exit(1)

from django.test import TestCase
from bharatfeed.models import TechArticle
from bharatfeed.pipeline import IngestionPipeline

class PipelineExecutionTests(TestCase):
    
    def setUp(self):
        self.pipeline = IngestionPipeline()
        # Mock payload structured exactly like a Dev.to API item response
        self.mock_item = {
            'title': '  Breaking: Next-Gen Quantum Architecture Disclosed  ',
            'url': 'https://example-tech-node.com/quantum-2026',
            'description': '<p>This is a raw text payload containing HTML elements.</p>',
            'tag_list': ['hardware', 'quantum']
        }

    def test_pipeline_sanitization_and_ingestion(self):
        # 1. Test raw text sanitization algorithm directly
        cleaned = self.pipeline.clean_text(self.mock_item['description'])
        self.assertFalse('<p>' in cleaned)
        self.assertFalse('</p>' in cleaned)

        # 2. Test database insertion via update_or_create
        title = self.mock_item['title'].strip()
        url = self.mock_item['url'].strip()
        body = self.mock_item['description']
        
        record, created = TechArticle.objects.update_or_create(
            source_url=url,
            defaults={
                'title': title,
                'content_raw': body,
                'cleaned_summary': self.pipeline.clean_text(body)[:500],
                'category': 'Global Tech Frontiers'
            }
        )
            
        self.assertEqual(record.title, 'Breaking: Next-Gen Quantum Architecture Disclosed')
        self.assertEqual(TechArticle.objects.count(), 1)
        
    def test_duplication_safety_boundary(self):
        url = self.mock_item['url'].strip()
        
        # Insert first record
        TechArticle.objects.update_or_create(
            source_url=url,
            defaults={
                'title': self.mock_item['title'].strip(),
                'content_raw': self.mock_item['description'],
                'cleaned_summary': self.pipeline.clean_text(self.mock_item['description'])[:500],
                'category': 'Global Tech Frontiers'
            }
        )
        
        # Attempt to insert identical source_url with a modified title
        updated_record, created = TechArticle.objects.update_or_create(
            source_url=url,
            defaults={
                'title': 'Updated Quantum Narrative',
                'content_raw': self.mock_item['description'],
                'cleaned_summary': self.pipeline.clean_text(self.mock_item['description'])[:500],
                'category': 'Global Tech Frontiers'
            }
        )
            
        # Assert database deduplication holds firm (count remains 1, title updates)
        self.assertEqual(TechArticle.objects.count(), 1)
        self.assertEqual(updated_record.title, 'Updated Quantum Narrative')

if __name__ == "__main__":
    from django.test.utils import get_runner
    from django.conf import settings 
    
    print("Initializing isolated local execution test suites for TechiePost...")
    
    TestRunner = get_runner(settings) 
    test_runner = TestRunner(verbosity=2, failfast=False)
    failures = test_runner.run_tests(["__main__"])
    if failures:
        sys.exit(1)