import axios from "axios";

export function getErrorMessage(error: unknown, fallback = "Unexpected error occurred."): string {
  if (axios.isAxiosError(error)) {
    const responseData = error.response?.data as Record<string, unknown> | undefined;
    if (typeof responseData === "string") {
      return responseData;
    }
    if (responseData) {
      if (typeof responseData.detail === "string") {
        return responseData.detail;
      }
      if (typeof responseData.error === "string") {
        return responseData.error;
      }
      if (Array.isArray(responseData.detail) && responseData.detail.length > 0) {
        const first = responseData.detail[0];
        if (typeof first === "string") {
          return first;
        }
      }
    }
    if (error.message) {
      return error.message;
    }
  }

  if (error instanceof Error) {
    return error.message || fallback;
  }

  return fallback;
}

export function toError(error: unknown, fallback?: string): Error {
  const message = getErrorMessage(error, fallback);
  return error instanceof Error ? Object.assign(error, { message }) : new Error(message);
}

