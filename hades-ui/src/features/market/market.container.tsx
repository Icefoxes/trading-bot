import { FC } from 'react';
import { useParams } from 'react-router-dom';
import { KLineComponent, AccountComponent } from '../../components';
import { useGetKlineQuery, useGetOrdersQuery, useGetPositionsQuery, useGetBalancesQuery } from '../../services';

export const MarketContainer: FC<{}> = () => {
    let { interval } = useParams();
    const { data } = useGetKlineQuery({ symbol: 'BTCUSDT', interval: interval || '1m' })
    const { data: orders } = useGetOrdersQuery({});
    const { data: positions } = useGetPositionsQuery({});
    const { data: balances } = useGetBalancesQuery({});
    return <div>
        <KLineComponent bars={data || []} />
        <AccountComponent orders={orders || []} positions={positions || []} balances={balances || []} />
    </div>
}