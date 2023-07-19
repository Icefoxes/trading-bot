import { FC } from "react";
import { KLineComponent } from '../../components';
import { useGetKlineQuery } from '../../services';

export const MarketContainer: FC<{}> = () => {
    const { data } = useGetKlineQuery({ symbol: 'BTC-USDT-SWAP', interval: '1m' })
    return <KLineComponent bars={data || []} />
}