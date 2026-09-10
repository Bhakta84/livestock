const API_BASE = "http://127.0.0.1:8000/api";

const asArray = (data, fallback = []) => {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  if (Array.isArray(data?.tenders)) return data.tenders;
  if (Array.isArray(data?.bids)) return data.bids;
  return fallback;
};

const errorMessage = (data, fallback) => {
  if (typeof data === "string") return data;
  if (data?.detail || data?.error || data?.message) return data.detail || data.error || data.message;
  if (data && typeof data === "object") return Object.entries(data).map(([field, value]) => `${field}: ${Array.isArray(value) ? value.join(", ") : value}`).join("; ");
  return fallback;
};

async function request(path, { method = "GET", token = null, body = undefined, params = {} } = {}) {
  const url = new URL(`${API_BASE}${path}`);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") url.searchParams.set(key, String(value));
  });

  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(url, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  const text = await response.text();
  if (!text) {
    throw new Error("Empty response from server.");
  }

  let data;
  try {
    data = JSON.parse(text);
  } catch (error) {
    throw new Error(`Invalid JSON response from server: ${text.slice(0, 200)}`);
  }

  if (!response.ok) {
    const error = new Error(errorMessage(data, "Request failed"));
    error.status = response.status;
    error.bidId = data?.bid_id;
    throw error;
  }

  return data;
}

export const register = async (payload) => {
  const form = new FormData();
  Object.entries(payload).forEach(([key, value]) => {
    if (value !== undefined && value !== null) form.append(key, value);
  });
  const response = await fetch(`${API_BASE}/auth/register/`, { method: "POST", body: form });
  const text = await response.text();
  let data;
  try { data = JSON.parse(text); } catch { throw new Error(`Registration failed with HTTP ${response.status}.`); }
  if (!response.ok) {
    const error = new Error(errorMessage(data, "Registration failed"));
    error.status = response.status;
    throw error;
  }
  return data;
};
export const login = (payload) => request("/auth/login/", { method: "POST", body: payload });

export const getTenders = (token) => request("/tenders/", { token }).then((x) => asArray(x));
export const getTender = (token, id) => request(`/tenders/${id}/`, { token });
export const getDocuments = (token, parent_id) => request(`/tenders/documents/`, { token, params: { tender: parent_id } });
export const createTenderItem = (token, payload) => request("/tenders/items/", { method: "POST", token, body: payload });
export const updateTender = (token, id, payload) => request(`/tenders/${id}/`, { method: "PATCH", token, body: payload });
export const updateTenderItem = (token, id, payload) => request(`/tenders/items/${id}/`, { method: "PATCH", token, body: payload });
export const deleteTenderItem = (token, id) => request(`/tenders/items/${id}/`, { method: "DELETE", token });
export const uploadTenderDocument = async (token, tenderId, file) => {
  const form = new FormData();
  form.append("tender", String(tenderId));
  form.append("name", file.name);
  form.append("file", file);
  const response = await fetch(`${API_BASE}/tenders/documents/`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });
  const text = await response.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    const error = new Error(`Document upload failed with HTTP ${response.status}. The server returned HTML instead of JSON.`);
    error.status = response.status;
    throw error;
  }
  if (!response.ok) {
    const error = new Error(errorMessage(data, "Document upload failed"));
    error.status = response.status;
    throw error;
  }
  return data;
};
export const getBOQ = (token, tender_id) => request(`/tenders/${tender_id}/`, { token });
export const getBids = (token) => request("/bids/", { token }).then((x) => asArray(x));
export const getBid = (token, id) => request(`/bids/${id}/`, { token });
export const createBid = (token, payload) => {
  const requestBody = { ...payload };
  if (requestBody.tender_id && !requestBody.tender) requestBody.tender = requestBody.tender_id;
  delete requestBody.tender_id;
  return request("/bids/", { method: "POST", token, body: requestBody });
};
export const saveBidItems = (token, payload) => request(`/bids/${payload.bid_id}/items/`, { method: "POST", token, body: payload });
export const submitBid = (token, id) => request(`/bids/${id}/submit/`, { method: "POST", token });
export const uploadDocument = async (token, payload) => {
  const form = new FormData();
  form.append("bid", String(payload.parent_id));
  form.append("name", payload.name);
  form.append("file", payload.file);
  const response = await fetch(`${API_BASE}/bids/documents/`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });
  const text = await response.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    const error = new Error(`Bid document upload failed with HTTP ${response.status}. The server returned HTML instead of JSON.`);
    error.status = response.status;
    throw error;
  }
  if (!response.ok) {
    const error = new Error(errorMessage(data, "Bid document upload failed"));
    error.status = response.status;
    throw error;
  }
  return data;
};
export const createTender = (token, payload) => request("/tenders/", { method: "POST", token, body: payload });
export const publishTender = (token, id) => request(`/tenders/${id}/publish/`, { method: "POST", token });
