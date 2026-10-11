import asyncio
from fastapi import APIRouter
from models.schemas import AnalyzeRequest, AnalyzeResponse
from services.virustotal import analyze_url
from services.ssl_checker import check_ssl
from services.ip_info import get_ip_info
from services.scorer import calculate_risk_score

# APIRouter = Express Router equivalent in Python
# prefix="/api" means all routes here start with /api
router = APIRouter(prefix="/api", tags=["analyze"])

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    url = request.url.strip()

    # Auto-fix missing scheme
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        # asyncio.gather() = runs coroutines CONCURRENTLY
        # Sequential (slow):  VT=2s → IP=1s → total 3s
        # With gather (fast): VT + IP fire together → total ~2s
        vt_result, ip_result = await asyncio.gather(
            analyze_url(url),
            get_ip_info(url),
        )

        # SSL is synchronous (uses socket, not async HTTP)
        ssl_result = check_ssl(url)

        score, label = calculate_risk_score(vt_result, ssl_result)

        return AnalyzeResponse(
            url         = url,
            risk_score  = score,
            risk_label  = label,
            score       = score,
            label       = label,
            virustotal  = vt_result,
            ssl         = ssl_result,
            ip_info     = ip_result,
        )

    except Exception as e:
        # Always return valid JSON — never let the API crash
        return AnalyzeResponse(
            url=url,
            risk_score=0,
            risk_label="Unknown",
            score=0,
            label="Unknown",
            error=str(e),
        )