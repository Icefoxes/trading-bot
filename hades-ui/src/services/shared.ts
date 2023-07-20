import { fetchBaseQuery } from "@reduxjs/toolkit/dist/query";

export const SiteBasicQuery = fetchBaseQuery({ baseUrl: process.env.REACT_APP_DOMAIN || 'http://localhost:8000/api/v1' });