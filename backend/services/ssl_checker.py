import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse
from models.schemas import SSLResult

def check_ssl(target: str) -> SSLResult:
    target = target.strip()
    port = 443

    if "://" in target:
        parsed = urlparse(target)
        hostname = parsed.hostname or ""
        if parsed.port:
            port = parsed.port
    elif "/" in target:
        hostname = target.split("/")[0].split(":")[0]
    elif ":" in target:
        parts = target.split(":")
        hostname = parts[0]
        try:
            port = int(parts[1])
        except ValueError:
            port = 443
    else:
        hostname = target

    if not hostname:
        return SSLResult(has_ssl=False, is_valid=False)

    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        # Extract subject (CN field)
        subject_dict = dict(x[0] for x in cert.get("subject", []))
        subject = subject_dict.get("commonName", hostname)

        # Extract issuer (organizationName or commonName)
        issuer_dict = dict(x[0] for x in cert.get("issuer", []))
        issuer = issuer_dict.get("organizationName") or issuer_dict.get("commonName") or "Unknown"

        # Parse expiry date — format: 'Dec 23 05:43:45 2026 GMT'
        expires_str = cert.get("notAfter", "")
        expires = ""
        days_remaining = None
        if expires_str:
            try:
                expires_dt = datetime.strptime(expires_str, "%b %d %H:%M:%S %Y %Z")
                expires = expires_dt.strftime("%Y-%m-%d")
                days_remaining = (expires_dt - datetime.utcnow()).days
            except Exception:
                expires = expires_str

        is_valid = True
        if days_remaining is not None and days_remaining < 0:
            is_valid = False

        return SSLResult(
            has_ssl=True,
            is_valid=is_valid,
            subject=subject,
            issuer=issuer,
            expires=expires,
            expires_on=expires,
            days_remaining=days_remaining,
        )

    except (ssl.SSLCertVerificationError, ssl.SSLError):
        # Connected to SSL port, but cert failed verification (expired, untrusted, self-signed)
        return SSLResult(
            has_ssl=True,
            is_valid=False,
            issuer="Untrusted / Invalid Certificate",
        )
    except Exception:
        # Cannot connect to port 443 (e.g. host down or plain HTTP only)
        return SSLResult(has_ssl=False, is_valid=False)