// Generic API client. Every feature-specific service (chatService.js,
// and future ones like documentService.js or knowledgeBaseService.js)
// should call through this instead of using `fetch` directly, so request
// setup, error handling and the base URL live in exactly one place.

import { API_BASE_URL } from "../../constants/config";

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request(path, options = {}) {
  let response;
  const isFormData = options.body instanceof FormData;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers: {
        // FormData sets its own Content-Type (with the multipart
        // boundary) — setting it ourselves would break the upload.
        ...(isFormData ? {} : { "Content-Type": "application/json" }),
        ...options.headers,
      },
    });
  } catch {
    throw new ApiError(
      "Could not reach the server. Check your connection and that the backend is running.",
      0
    );
  }

  if (!response.ok) {
    const message = await extractErrorMessage(response);
    throw new ApiError(message, response.status);
  }

  if (response.status === 204) return null;

  return response.json();
}

async function extractErrorMessage(response) {
  try {
    const data = await response.json();
    if (typeof data.detail === "string") return data.detail;
    if (Array.isArray(data.detail) && data.detail[0]?.msg) {
      return data.detail[0].msg;
    }
  } catch {
    // response body wasn't JSON; fall through to the generic message
  }
  return `Request failed with status ${response.status}.`;
}

export const apiClient = {
  post: (path, body) =>
    request(path, { method: "POST", body: JSON.stringify(body) }),
  postForm: (path, formData) => request(path, { method: "POST", body: formData }),
  get: (path) => request(path, { method: "GET" }),
  delete: (path) => request(path, { method: "DELETE" }),
};