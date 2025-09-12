export const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000';

// Debug: Log the API base URL and environment variables
console.log('API_BASE:', API_BASE);
console.log('import.meta.env:', import.meta.env);

export async function post<TReq, TRes>(path: string, body: TReq): Promise<TRes> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`POST ${path} failed: ${res.status} ${txt}`);
  }
  return res.json();
}
