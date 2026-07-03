import json
import urllib.request
import re
import logging
from .models import TechArticle

# Instantiating a named logger specific to this application module
logger = logging.getLogger(__name__)

class IngestionPipeline:
    def __init__(self):
        self.api_url = "https://dev.to/api/articles?per_page=10"
        self.user_agent = "TechiePostDataEngine/1.0"

    def clean_text(self, text):
        if not text:
            return ""
        cleaned = re.sub(r'<[^>]+>', '', text)
        return " ".join(cleaned.split())

    def fetch_live_feeds(self):
        request = urllib.request.Request(
            self.api_url, 
            headers={'User-Agent': self.user_agent}
        )
        
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                if response.status == 200:
                    return json.loads(response.read().decode('utf-8'))
                
                logger.warning(f"Unexpected API response status received: {response.status}")
        except Exception as network_err:
            logger.error(f"Network request transaction terminated: {str(network_err)}")
            return []

    def run_sync_cycle(self):
        raw_items = self.fetch_live_feeds()
        ingested_records = []

        if not raw_items:
            logger.info("Sync cycle completed: No fresh payloads received from upstream remote.")
            return 0

        for item in raw_items:
            title = item.get('title', '').strip()
            url = item.get('url', '').strip()
            body = item.get('description', '') or item.get('title', '')
            tags = item.get('tag_list', [])
            
            if not title or not url:
                continue

            is_local = any(tag.lower() in ['india', 'bharat', 'bengaluru', 'pune'] for tag in tags)
            assigned_category = 'BharatFeed' if is_local else 'Global Tech Frontiers'

            try:
                article, created = TechArticle.objects.update_or_create(
                    source_url=url,
                    defaults={
                        'title': title,
                        'content_raw': body,
                        'cleaned_summary': self.clean_text(body)[:500],
                        'category': assigned_category
                    }
                )
                ingested_records.append(article)
            except Exception as db_err:
                logger.error(f"Database insertion write failed for URL [{url}]: {str(db_err)}")
                
        logger.info(f"Ingestion lifecycle finished. Processed updates: {len(ingested_records)}")
        return len(ingested_records)