import { useState } from "react";

export default function URLInput({ onAnalyze, loading}){
    const [url, setUrl] = useState('')

    const handleSubmit = (e) => {
        e.preventDefault()
        if(url.trim()){
            onAnalyze(url.trim())
        }
    }

    return(
        <form onSubmit={handleSubmit} className="input-form">
            <div className="input-row">
                <input type="text" value={url} onChange={(e) => setUrl(e.target.value)} placeholder="https://example.com" className="url-input" disabled={loading}/>
                <button type="submit" className="analyze-btn" disabled={loading || !url.trim()}>{loading ? "Analyzing..." : "Analyze"}</button>
            </div>
        </form>
    );
}