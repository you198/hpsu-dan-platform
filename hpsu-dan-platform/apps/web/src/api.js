function token() { return localStorage.getItem('access_token') || ''; }
export async function api(path, options = {}) {
    const headers = new Headers(options.headers);
    if (!(options.body instanceof FormData))
        headers.set('Content-Type', 'application/json');
    if (token())
        headers.set('Authorization', `Bearer ${token()}`);
    const response = await fetch(`/api/v1${path}`, { ...options, headers });
    if (!response.ok)
        throw new Error((await response.json().catch(() => ({}))).detail || `HTTP_${response.status}`);
    return response.json();
}
export function chatWithAssistant(content) {
    return api('/assistant/chat', {
        method: 'POST',
        body: JSON.stringify({
            messages: [{ role: 'user', content }],
            temperature: 0.2,
            max_tokens: 1200,
        }),
    });
}
