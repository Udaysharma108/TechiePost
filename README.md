# TechiePost

A decoupled backend data pipeline and aggregation architecture developed in Django. Data ingestion happens through polling of remote engineering logs via public REST APIs; cleansing and normalization of raw text payloads through regex sanitation layers; and classification of streams into target regional/global feeds via matrix of tags.

---

## 🏗️ Core System Architecture

The application architecture consists of completely decoupled modules for the sake of isolating data ingestion from client-side presentations.

* **Ingestion Pipeline (`bharatfeed/pipeline.py`)**: Independent ETL Engine that uses Python `urllib.request` for streaming data to enable remote handshaking. This allows us to avoid third-party request libraries.
* **Decoupled Rest API Layer (`bharatfeed/views.py`)**: Serves serialized logs from database as JSON configurations complete with transaction details in the form of payload metrics.
* **Asynchronous Client Dashboard (`dashboard.html`)**: Terminal style client-side single page asynchronous UI that queries APIs and parses classification matrices.

---

## 📊 Database Schema & Performance Engineering

The schema strictly follows constraint to account for data integrity and ensure no duplicates records while frequent syncing.

### Model: `TechArticle` (Table: `tech_articles`)

| Field Name | Data Type   | Configuration / Constraints    | Functional Purpose                       |
| :--- | :--- | :--- | :--- |
| `id`          | BigAutoField  | Primary Key (Auto)            | Unique system identifier               |
| `title`       | CharField     | `max_length=255`              | Sanitized title of the source log      |
| `source_url`  | URLField     | `unique=True`                 | Duplication blocking at the engine level|
| `content_raw` | TextField    | —                             | Original unparsed content string       |
| `cleaned_summary`  | TextField | `blank=True, null=True`       | Regex-stripped textual summary snippet |
| `category`     | CharField    | `max_length=100`, default assigned | Internal router designation (`BharatFeed` / `Global`) |
| `fetched_at` | DateTimeField| `default=timezone.now`         | Internal pipeline transaction timestamp |

### Database Optimization
To safeguard lookup efficiency from scalability, the application employs explicit index arrays within the `Meta` runtime configuration class:
* **Index 1:** `source_url` field for speedy `update_or_create` upsert operation evaluation.
* **Index 2:** `fetched_at` field to optimize descending sort operations on the date during API exposition.

---
## 🛠️ Telemetry and System Logs

As against writing plain log strings using `print()` to `stdout` stream, the whole pipeline relies on the built-in `logging` matrix of Python.

```python
import logging
logger = logging.getLogger(__name__)

# Monitor operational exceptions without stopping thread execution
logger.error(f"Failed database insert for URL [{url}]: {str(db_err)}")
