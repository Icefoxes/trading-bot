import { FC, useState } from 'react';
import { KLineComponent, AccountComponent } from '../../components';
import { useGetKlineQuery, useGetOrdersQuery, useGetPositionsQuery, useGetBalancesQuery } from '../../services';

export const MarketContainer: FC<{}> = () => {
    const [interval, setInterval] = useState<string>('1m');
    const { data } = useGetKlineQuery({ symbol: 'BTCUSDT', interval: interval })
    const { data: orders } = useGetOrdersQuery({});
    const { data: positions } = useGetPositionsQuery({});
    const { data: balances } = useGetBalancesQuery({});
    return <>
        <KLineComponent bars={data || []}
            orders={orders || []}
            positions={positions || []}
            onIntervalChanged={setInterval} />
        <AccountComponent orders={orders || []} positions={positions || []} balances={balances || []} />
    </>
}