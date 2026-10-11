import httpx, base64, os
from urllib.parse import urlparse
from models.schemas import VirusTotalResult

VT_BASE = "https://www.virustotal.com/api/v3"

def _encode_url(url: str) -> str:
    url_bytes = url.encode()
    b64_bytes = base64.urlsafe_b64encode(url_bytes)
    return b64_bytes.decode().rstrip("=")

async def analyze_url(url: str) -> VirusTotalResult | None:
    api_key = os.getenv("VIRUSTOTAL_API_KEY", "")
    if not api_key:
        return None

    encoded = _encode_url(url)
    endpoint = f"{VT_BASE}/urls/{encoded}"
    headers = {"x-apikey": api_key}

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(endpoint, headers=headers)

        # If specific URL is not yet indexed (404), fall back to domain analysis
        if response.status_code == 404:
            # Trigger analysis for the URL in background so it's indexed for later
            try:
                await client.post(f"{VT_BASE}/urls", headers=headers, data={"url": url})
            except Exception:
                pass

            domain = urlparse(url).hostname
            if domain:
                domain_endpoint = f"{VT_BASE}/domains/{domain}"
                response = await client.get(domain_endpoint, headers=headers)

    if response.status_code != 200:
        return None

    data = response.json()
    attributes = data.get("data", {}).get("attributes", {})
    stats = attributes.get("last_analysis_stats", {})
    results = attributes.get("last_analysis_results", {})

    # Collect names of threats found
    threat_names = [
        info["result"]
        for info in results.values()
        if info.get("category") in ("malicious", "suspicious") and info.get("result")
    ]
    threat_names = list(dict.fromkeys(threat_names))

    total = sum(stats.values())

    return VirusTotalResult(
        malicious=stats.get("malicious", 0),
        suspicious=stats.get("suspicious", 0),
        harmless=stats.get("harmless", 0),
        undetected=stats.get("undetected", 0),
        total_engines=total,
        total_engine=total,
        threat_names=threat_names[:5],
    )