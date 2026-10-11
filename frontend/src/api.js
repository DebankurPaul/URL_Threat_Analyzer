const BASE_URL = ''   // empty string = same host, nginx handles routing

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