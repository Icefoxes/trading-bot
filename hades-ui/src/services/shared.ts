import { fetchBaseQuery } from "@reduxjs/toolkit/dist/query";

export const SiteBasicQuery = fetchBaseQuery({ baseUrl: process.env.HOST || 'http://localhost:8000/api/v1' });