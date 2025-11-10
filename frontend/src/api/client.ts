import axios from "axios";

export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
});

export type Paginated<T> = {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
};
