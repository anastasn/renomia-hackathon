/**
 * Thin API client for the FastAPI backend.
 * Base URL is proxied through Next.js rewrites in next.config.ts.
 * In production, set NEXT_PUBLIC_API_URL in your environment.
 */

 const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:5001";

export interface HealthResponse {
  status: string;
  version: string;
  services: Record<string, string>;
}

export async function fetchHealth(): Promise<HealthResponse> {
  console.debug(`Fetching health from ${BACKEND_URL}/api/health`);
  const res = await fetch(`${BACKEND_URL}/api/health`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Backend returned ${res.status}`);
  return res.json() as Promise<HealthResponse>;
}

// ------------------------------------------------------------
// Add your domain-specific API calls below.
// Example:
//
// export async function createDocument(payload: CreateDocumentDto) {
//   const res = await fetch(`${BASE}/documents`, {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify(payload),
//   });
//   if (!res.ok) throw new Error(`Failed to create document: ${res.status}`);
//   return res.json();
// }
// ------------------------------------------------------------
