from pydantic import BaseModel
from typing import Optional

class AnalyzeRequest(BaseModel):
    url : str

class VirusTotalResult(BaseModel):
    malicious : int = 0
    suspicious : int = 0
    harmless : int = 0
    undetected : int = 0
    total_engines : int = 0
    total_engine : Optional[int] = None
    threat_names : list[str] = []

class SSLResult(BaseModel):
    has_ssl: bool
    subject: Optional[str] = None
    issuer: Optional[str] = None     
    expires: Optional[str] = None
    expires_on: Optional[str] = None
    days_remaining: Optional[int] = None
    is_valid: bool = False

class AnalyzeResponse(BaseModel):
    url : str
    risk_score : int
    risk_label : str
    score: Optional[int] = None
    label: Optional[str] = None
    virustotal : Optional[VirusTotalResult] = None
    ssl: Optional[SSLResult] = None
    ip_info: Optional[dict] = None
    error: Optional[str] = None