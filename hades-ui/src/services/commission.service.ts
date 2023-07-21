import { createApi } from '@reduxjs/toolkit/query/react';
import { SiteBasicQuery } from './shared';
import { Trade } from '../models';


export const commissionApi = createApi({
    reducerPath: 'commissionApi',
    baseQuery: SiteBasicQuery,
    endpoints: (builder) => ({
        getTrades: builder.query<Trade[], { symbol: string }>({
            query: ({ symbol }) => `trades?symbol=${symbol}`,
        }),
    }),
})

export const {
    useGetTradesQuery
} = commissionApi;