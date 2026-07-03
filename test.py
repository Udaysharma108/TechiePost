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
        self.mock_payload = {
            'title': '  Breaking: Next-Gen Quantum Architecture Disclosed  ',
            'url': 'https://example-tech-node.com/quantum-2026',
            'content': '<p>This is a raw text payload containing HTML elements.</p>',
            'category': 'Hardware Systems'
        }

    def test_pipeline_sanitization_and_ingestion(self):
        record = self.pipeline.process_and_save(self.mock_payload)
        
        # 1. This explicit check satisfies Pylance that 'record' is definitely not None
        if record is None:
            self.fail("Pipeline returned None, expected a TechArticle instance.")
            
        self.assertEqual(record.title, 'Breaking: Next-Gen Quantum Architecture Disclosed')
        
        # 2. Use an empty string fallback so Pylance knows it's evaluating 'str in str'
        summary = record.cleaned_summary or ""
        self.assertFalse('<p>' in summary)
        self.assertEqual(TechArticle.objects.count(), 1)
        
        
    def test_duplication_safety_boundary(self):
        self.pipeline.process_and_save(self.mock_payload)
        
        modified_payload = self.mock_payload.copy()
        modified_payload['title'] = 'Updated Quantum Narrative'
        
        updated_record = self.pipeline.process_and_save(modified_payload)
        
        # Satisfy Pylance type-checking
        if updated_record is None:
            self.fail("Pipeline returned None on update.")
            
        self.assertEqual(TechArticle.objects.count(), 1)
        self.assertEqual(updated_record.title, 'Updated Quantum Narrative')

if __name__ == "__main__":
    from django.test.utils import get_runner
    from django.conf import settings  # <--- Import settings explicitly here
    
    print("Initializing isolated local execution test suites for TechiePost...")
    
    # Use the explicitly imported settings object
    TestRunner = get_runner(settings) 
    test_runner = TestRunner(verbosity=2, failfast=False)
    failures = test_runner.run_tests(["__main__"])
    if failures:
        sys.exit(1)