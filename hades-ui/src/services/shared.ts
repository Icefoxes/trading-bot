import { fetchBaseQuery } from "@reduxjs/toolkit/dist/query";

export const SiteBasicQuery = fetchBaseQuery({ baseUrl: 'http://localhost:8000/api/v1' });