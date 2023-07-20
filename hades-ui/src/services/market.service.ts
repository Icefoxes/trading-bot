import { createApi } from '@reduxjs/toolkit/query/react';
import { SiteBasicQuery } from './shared';
import { Kline, Order, Position, Balance } from '../models';


export const marketApi = createApi({
    reducerPath: 'marketApi',
    baseQuery: SiteBasicQuery,
    endpoints: (builder) => ({
        getKline: builder.query<Kline[], { symbol: string, interval: string }>({
            query: ({ interval, symbol }) => `klines?symbol=${symbol}&interval=${interval}&limit=300`,
        }),
        getOrders: builder.query<Order[], {}>({
            query: () => `orders`,
        }),
        getPositions: builder.query<Position[], {}>({
            query: () => `positions`,
        }),
        getBalances: builder.query<Balance[], {}>({
            query: () => `balances`,
        }),
    }),
})


export const {
    useGetKlineQuery,
    useGetOrdersQuery,
    useGetPositionsQuery,
    useGetBalancesQuery
} = marketApi;