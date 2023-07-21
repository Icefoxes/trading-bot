import { FC } from "react";
import { Card } from "antd";
import moment from 'moment';

import { useGetTradesQuery } from "../../services";
import { TradeDetailComponent } from '../../components';
import './commission.container.scss';


export const CommissionContainer: FC<{}> = () => {
    const { data: trades } = useGetTradesQuery({ symbol: 'BTCUSDT' });
    const filterTrades = (trades || []).filter(trade => moment().date() === moment(trade.timestamp).date());
    //  console.log(filterTrades)
    return <>
        <div className="card-container">
            <Card title="Trades Today" bordered={false}>
                {new Set(filterTrades.map(f => f.orderId)).size}
            </Card>

            <Card title="Commission Today" bordered={false}>
                {filterTrades.map(t => t.commissionToUSDT).reduce((prev, next) => prev + next, 0).toFixed(3)}
            </Card>

            <Card title="PNL Today" bordered={false}>
                {filterTrades.map(t => t.realizedPnl).reduce((prev, next) => prev + next, 0).toFixed(3)}
            </Card>
        </div>
        <TradeDetailComponent trades={filterTrades || []} />
    </>
}