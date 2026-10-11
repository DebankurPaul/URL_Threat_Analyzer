// src/components/ResultCard.jsx
export default function ResultCard({ title, icon, children }) {
  return (
    <div className="result-card">
      <div className="card-header">
        <span className="card-icon">{icon}</span>
        <h3>{title}</h3>
      </div>
      <div className="card-body">
        {children}
      </div>
    </div>
  )
}

// Small reusable row inside a card
export function InfoRow({ label, value, highlight }) {
  return (
    <div className="info-row">
      <span className="info-label">{label}</span>
      <span className={`info-value ${highlight || ''}`}>{value}</span>
    </div>
  )
}