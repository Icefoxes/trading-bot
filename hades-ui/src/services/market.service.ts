import { createApi } from '@reduxjs/toolkit/query/react';
import { SiteBasicQuery } from './shared';
import { Kline } from '../models';


export const marketApi = createApi({
    reducerPath: 'marketApi',
    baseQuery: SiteBasicQuery,
    endpoints: (builder) => ({
        getKline: builder.query<Kline[], { symbol: string, interval: string }>({
            query: ({ interval, symbol }) => `klines?symbol=${symbol}&interval=${interval}&limit=200`,
        }),
    }),
})


export const {
    useGetKlineQuery
} = marketApi;