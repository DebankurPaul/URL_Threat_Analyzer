import httpx, socket, os
from urllib.parse import urlparse

async def get_ip_info(url: str) -> dict | None:
    parsed   = urlparse(url)
    hostname = parsed.hostname
    if not hostname: return None

    try:
        # DNS lookup: "google.com" → "142.250.x.x"
        # This is exactly what happens when you type a URL in a browser
        ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        return None   # DNS failed — domain doesn't exist

    api_key  = os.getenv("IPINFO_API_KEY", "")
    endpoint = f"https://ipinfo.io/{ip}/json"
    params   = {"token": api_key} if api_key else {}

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(endpoint, params=params)

    if response.status_code != 200:
        return {"ip": ip}   # return at least the IP

    data = response.json()
    return {
        "ip"      : data.get("ip"),
        "city"    : data.get("city"),
        "region"  : data.get("region"),
        "country" : data.get("country"),
        "org"     : data.get("org"),      # e.g. "AS15169 Google LLC"
        "hostname": data.get("hostname"),
    }