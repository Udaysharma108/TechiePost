from django.http import JsonResponse
from django.shortcuts import render  # Grouped neatly at the top
from .models import TechArticle

def feed_endpoint(request):
    """
    Exposes parsed technology logs partitioned by internal routing categories.
    """
    # Fetch latest entries for both channels
    global_items = TechArticle.objects.filter(category='Global Tech Frontiers')[:15]
    local_items = TechArticle.objects.filter(category='BharatFeed')[:15]

    # Structure data records into lightweight dictionary blocks
    payload = {
        "status": "success",
        "metrics": {
            "total_global": global_items.count(),
            "total_bharat": local_items.count()
        },
        "feeds": {
            "global_tech_frontiers": [
                {
                    "title": item.title,
                    "url": item.source_url,
                    "summary": item.cleaned_summary,
                    "published": item.published_at.isoformat() if item.published_at else None
                }
                for item in global_items
            ],
            "bharat_feed": [
                {
                    "title": item.title,
                    "url": item.source_url,
                    "summary": item.cleaned_summary,
                    "published": item.published_at.isoformat() if item.published_at else None
                }
                for item in local_items
            ]
        }
    }

    # Return structured payload with safe cross-origin handling indicators if needed
    return JsonResponse(payload, safe=False, json_dumps_params={'indent': 2})


def dashboard_view(request):
    """
    Renders the central system monitoring and feed interface dashboard.
    """
    return render(request, 'bharatfeed/dashboard.html')