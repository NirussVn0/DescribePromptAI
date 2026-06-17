import axios from "axios";

import { toError } from "../utils/errors";

const instance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
});

export const apiClient = {
  async get<T>(url: string) {
    try {
      const response = await instance.get<T>(url);
      return response.data;
    } catch (error) {
      throw toError(error);
    }
  },
  async post<T>(url: string, data: unknown) {
    try {
      const response = await instance.post<T>(url, data);
      return response.data;
    } catch (error) {
      throw toError(error);
    }
  }
};
