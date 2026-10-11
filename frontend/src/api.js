const BASE_URL = 'https://url-threat-analyzer-backend.onrender.com'   // empty string = same host, nginx handles routing

async function parseJsonResponse(response) {
    const text = await response.text()

    if (!text) {
        return null
    }

    try {
        return JSON.parse(text)
    } catch {
        return null
    }
}

export async function analyzeURL(url) {
    const response = await fetch(`${BASE_URL}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
    })
    if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Analysis failed')
    }
    return response.json()
}