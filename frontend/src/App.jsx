// src/App.jsx
import { useState } from 'react'
import { analyzeURL } from './api'
import URLInput from '../components/URLInput'
import ScoreMeter from '../components/ScoreMeter'
import ResultCard, { InfoRow } from '../components/ResultCard'
import './App.css'

export default function App() {
  const [loading, setLoading] = useState(false)
  const [result, setResult]   = useState(null)
  const [error, setError]     = useState(null)

  async function handleAnalyze(url) {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await analyzeURL(url)
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)   // always runs, even if error
    }
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <h1>🛡️ URL Threat Analyzer</h1>
        <p>Check any URL for malware, phishing, and security threats</p>
      </header>

      {/* Input */}
      <URLInput onAnalyze={handleAnalyze} loading={loading} />

      {/* Loading state */}
      {loading && (
        <div className="loading">
          <div className="spinner" />
          <p>Running security checks...</p>
        </div>
      )}

      {/* Error state */}
      {error && (
        <div className="error-box">
          ⚠️ {error}
        </div>
      )}

      {/* Results */}
      {result && (
  <div className="results">
    {/* Risk Score */}
    <div className="score-section">
      <ScoreMeter score={result.score ?? result.risk_score ?? 0} label={result.label ?? result.risk_label ?? 'Unknown'} />
    </div>

    <div className="cards-grid">
      {/* VirusTotal Card */}
      <ResultCard title="VirusTotal" icon="🦠">
        {result.virustotal ? (
          <>
            <InfoRow label="Malicious engines"
              value={result.virustotal.malicious}
              highlight={result.virustotal.malicious > 0 ? 'danger' : 'safe'} />
            <InfoRow label="Suspicious engines"
              value={result.virustotal.suspicious} />
            <InfoRow label="Total engines scanned"
              value={result.virustotal.total_engines ?? result.virustotal.total_engine ?? 0} />
            {result.virustotal.threat_names?.length > 0 && (
              <div className="threat-tags">
                {result.virustotal.threat_names.map(name => (
                  <span key={name} className="threat-tag">{name}</span>
                ))}
              </div>
            )}
          </>
        ) : <p className="no-data">No VirusTotal data available</p>}
      </ResultCard>

      {/* SSL Card */}
      <ResultCard title="SSL Certificate" icon="🔒">
        {result.ssl ? (
          <>
            <InfoRow label="Has SSL"
              value={result.ssl.has_ssl ? 'Yes ✅' : 'No ❌'}
              highlight={result.ssl.has_ssl ? 'safe' : 'danger'} />
            {result.ssl.has_ssl && (
              <>
                <InfoRow label="Issued to"    value={result.ssl.subject || '—'} />
                <InfoRow label="Issuer"       value={result.ssl.issuer || '—'} />
                <InfoRow label="Expires"      value={result.ssl.expires || '—'} />
                <InfoRow label="Days left"    value={result.ssl.days_remaining ?? '—'} />
              </>
            )}
          </>
        ) : <p className="no-data">SSL check failed</p>}
      </ResultCard>

      {/* IP Info Card */}
      <ResultCard title="IP Information" icon="🌍">
        {result.ip_info ? (
          <>
            <InfoRow label="IP Address" value={result.ip_info.ip || '—'} />
            <InfoRow label="Country"    value={result.ip_info.country || '—'} />
            <InfoRow label="City"       value={result.ip_info.city || '—'} />
            <InfoRow label="ISP / Org"  value={result.ip_info.org || '—'} />
          </>
        ) : <p className="no-data">IP lookup failed</p>}
      </ResultCard>
    </div>
  </div>
)}
    </div>
  )
}