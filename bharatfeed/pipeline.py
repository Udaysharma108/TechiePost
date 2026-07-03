import json
import urllib.request
import re  # Fixes: "re" is not defined
import logging  # Fixes: "logger" is not defined
from .models import TechArticle  # Fixes: "TechArticle" is not defined
from .constants import BHARAT_TECH_MATRIX  # Fixes: "BHARAT_TECH_MATRIX" is not defined

# Initialize the logger instance module properly
logger = logging.getLogger(__name__)

class IngestionPipeline:
    def __init__(self):
        self.hn_top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        self.hn_item_base_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"
        self.devto_url = "https://dev.to/api/articles?latest=true&per_page=100"  
        self.user_agent = "TechieNewsDataEngine/1.0"

    def clean_text(self, text):
        if not text:
            return ""
        cleaned = re.sub(r'<[^>]+>', '', text)
        return " ".join(cleaned.split())

    def extractive_nlp_summarizer(self, text, sentence_count=3):
        if not text or len(text.strip()) < 80:
            return text
        clean_text = self.clean_text(text)
        sentences = re.split(r'(?<=[.!?])\s+', clean_text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        if len(sentences) <= sentence_count:
            return " ".join(sentences)
        return " ".join(sentences[:sentence_count])

    def fetch_json(self, url):
        request = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
        try:
            with urllib.request.urlopen(request, timeout=8) as response:
                if response.status == 200:
                    return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            logger.error(f"Network error on [{url}]: {str(e)}")
        return None

    def sync_global_hacker_news(self):
        top_story_ids = self.fetch_json(self.hn_top_stories_url)
        if not top_story_ids:
            return 0

        count = 0
        for story_id in top_story_ids[:15]:  
            item_data = self.fetch_json(self.hn_item_base_url.format(story_id))
            if not item_data or 'title' not in item_data:
                continue

            title = item_data.get('title', '').strip()
            url = item_data.get('url') or f"https://news.ycombinator.com/item?id={story_id}"
            score = item_data.get('score', 0)
            author = item_data.get('by', 'anonymous')
            
            domain_match = re.search(r'https?://([^/]+)', url)
            domain = domain_match.group(1) if domain_match else "TechieNews Core"

            rich_summary = (
                f"This architectural briefing covers critical software insights regarding '{title}'. "
                f"Originally brought to light by engineering contributor '{author}', the technical concepts are generating "
                f"substantial discussion across development networks on '{domain}'. The engineering community has rallied a "
                f"strong community tracking metric score of {score} points around this development. Select the read option "
                f"below to examine the comprehensive implementation details."
            )

            TechArticle.objects.update_or_create(
                source_url=url,
                defaults={
                    'title': title,
                    'content_raw': rich_summary,
                    'cleaned_summary': rich_summary,
                    'category': 'Global Tech Frontiers'
                }
            )
            count += 1
        return count

    def sync_regional_devto(self):
        """
        Harvests regional tech ecosystem updates using advanced contextual token 
        validation to filter out explicit spam, adult content, and lifestyle noise.
        """
        search_queries = [
            "india", "bharat", "bengaluru", "bangalore", "pune", "mumbai", 
            "delhi", "hyderabad", "tcs", "infosys", "wipro", "isro", "upi"
        ]
        
        # Target exact high-noise phrases used by SEO spammers
        EXPLICIT_SPAM_PHRASES = [
            'escort service', 'callgirl in', 'call girl', 'independent escorts',
            'adult dating', 'male fertility doctor', 'best radiologist', 
            'hot webseries', 'watch online', 'adult links', '18+ link'
        ]
        
        # Structural tokens targeting pornographic, explicit, or highly unprofessional noise
        ADULT_SPAM_MATRIX = {
            'porn', 'pornsite', 'sextoy', 'sextoys', 'xrated', 'xxx', 'erotic', 
            'sensual', 'webseries', 'episodes', 'streaming'
        }
        
        count = 0
        ingested_urls = set()

        logger.info("[Pipeline] Running Advanced Integrity Filtering for BharatFeed...")

        for query in search_queries:
            if count >= 10:  
                break
                
            search_url = f"https://dev.to/api/articles?tag={query}&per_page=20"
            raw_items = self.fetch_json(search_url)
            
            if not raw_items:
                continue

            for item in raw_items:
                title = item.get('title', '').strip()
                url = item.get('url', '').strip()
                body = item.get('description', '') or item.get('title', '')
                tags = [t.lower() for t in item.get('tag_list', [])]
                author_name = item.get('user', {}).get('name', 'TechieNews Contributor')

                if url in ingested_urls:
                    continue

                # 1. Immediate Spam Phrase Gate
                searchable_text = f"{title} {body} {' '.join(tags)}".lower()
                if any(phrase in searchable_text for phrase in EXPLICIT_SPAM_PHRASES):
                    continue  

                # 2. Tokenize text content down to lowercase words
                words_in_article = set(re.findall(r'[a-z0-9]+', searchable_text))

                # 3. Direct Adult Content & Explicit Term Filter Gate
                if not words_in_article.isdisjoint(ADULT_SPAM_MATRIX):
                    continue  # Instantly drops any post infected with explicit keywords

                # Gate A: Must contain a verified regional tracking identifier
                has_regional_node = not words_in_article.isdisjoint(BHARAT_TECH_MATRIX)
                
                # Gate B: Confirm it belongs in a tech context (tags or titles)
                tech_tags = {'webdev', 'javascript', 'python', 'react', 'node', 'devops', 'ai', 'ml', 'database', 'coding', 'software', 'engineering', 'opensource'}
                has_tech_tag = not set(tags).isdisjoint(tech_tags)
                is_tech_title = any(word in title.lower() for word in ['built', 'app', 'tool', 'system', 'code', 'software', 'engineering', 'tech', 'hiring', 'developer', 'open source'])

                if has_regional_node and (has_tech_tag or is_tech_title):
                    
                    # Generate a clean, humanized, high-density summary paragraph
                    rich_summary = (
                        f"This ecosystem insight highlights technical engineering progress concerning '{title}'. "
                        f"Documented by industry contributor '{author_name}', the analysis explores key software architecture implementations "
                        f"and structural code updates shaping up across regional developer teams. The milestone delivers highly valuable, "
                        f"actionable patterns for technical specialists navigating modern infrastructure frameworks. Select the read option "
                        f"below to review the complete implementation."
                    )
                    
                    # Handle sensitive systemic key identifiers gracefully via generic descriptive placeholders
                    if "aadhaar" in searchable_text:
                        rich_summary = rich_summary.replace("Aadhaar", "[Identity System Verification Active]")

                    TechArticle.objects.update_or_create(
                        source_url=url,
                        defaults={
                            'title': title,
                            'content_raw': body,
                            'cleaned_summary': rich_summary,
                            'category': 'BharatFeed'
                        }
                    )
                    ingested_urls.add(url)
                    count += 1
                    
                    if count >= 10:
                        break
                        
        return count

    def run_sync_cycle(self):
        logger.info("[Pipeline] Running dual-stream data ingestion cycle...")
        hn_count = self.sync_global_hacker_news()
        devto_count = self.sync_regional_devto()
        return hn_count + devto_count