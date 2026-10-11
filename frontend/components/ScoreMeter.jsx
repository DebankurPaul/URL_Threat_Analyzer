// src/components/ScoreMeter.jsx
export default function ScoreMeter({ score, label }) {
  const radius = 54
  const circumference = 2 * Math.PI * radius

  // For score=0, show at least a tiny fill so circle isn't invisible
  const displayScore = score ?? 0
  const filled = (displayScore / 100) * circumference

  const color =
    label === 'Safe' ? '#3fb950' :
    label === 'Suspicious' ? '#f0883e' :
    label === 'Dangerous' ? '#ff7b72' :
    (displayScore >= 85 ? '#3fb950' : displayScore >= 50 ? '#f0883e' : '#ff7b72')

  return (
    <div className="score-meter">
      <svg width="140" height="140" viewBox="0 0 140 140">
        {/* Grey background track */}
        <circle
          cx="70" cy="70" r={radius}
          fill="none"
          stroke="#30363d"
          strokeWidth="10"
        />
        {/* Colored fill — only render if score > 0 */}
        {displayScore > 0 && (
          <circle
            cx="70" cy="70" r={radius}
            fill="none"
            stroke={color}
            strokeWidth="10"
            strokeDasharray={`${filled} ${circumference}`}
            strokeLinecap="round"
            transform="rotate(-90 70 70)"
            style={{ transition: 'stroke-dasharray 0.8s ease' }}
          />
        )}
        {/* Score number — always shows */}
        <text
          x="70" y="65"
          textAnchor="middle"
          fontSize="28"
          fontWeight="700"
          fill={color}
        >
          {displayScore}
        </text>
        {/* /100 below the number */}
        <text
          x="70" y="84"
          textAnchor="middle"
          fontSize="12"
          fill="#8b949e"
        >
          /100
        </text>
      </svg>
      <div className="score-label" style={{ color }}>
        {label}
      </div>
    </div>
  )
}