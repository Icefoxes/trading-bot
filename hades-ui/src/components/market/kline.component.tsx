import { useRef, useEffect, FC } from 'react';
import { Chart, init, dispose } from 'klinecharts';
import { Radio } from 'antd';
import moment from 'moment';

import { Kline, Order, Position } from '../../models';


export const KLineComponent: FC<{
    bars: Kline[],
    orders: Order[],
    positions: Position[],
    onIntervalChanged: (interval: string) => void
}> = ({ bars, orders, positions, onIntervalChanged }) => {
    useEffect(() => {
        if (bars.length > 0) {
            document.title = `${bars[bars.length - 1]?.close}`;
        }
    }, [bars]);
    useEffect(() => {
        const data = bars.map(bar => {
            return {
                timestamp: moment(bar.timestamp).unix() * 1000,
                open: bar.open,
                close: bar.close,
                high: bar.high,
                low: bar.low,
                volume: bar.vol
            };
        });
        if (data.length > 0) {
            chart.current = init('hades-klines-chart');
            chart.current?.createIndicator('VOL');
            orders.forEach(order => {
                chart.current?.createOverlay({
                    name: 'simpleAnnotation',
                    extendData: order.side,
                    points: [{ timestamp: moment(order.timestamp).unix() * 1000, value: order.price }]
                });
                chart.current?.createOverlay({
                    name: 'simpleTag',
                    extendData: order.side,
                    points: [{ value: order.price }]
                })
            })
            positions.forEach(pos => {
                chart.current?.createOverlay({
                    name: 'simpleTag',
                    extendData: `${pos.unrealized_profit}`,
                    points: [{ value: pos.price }]
                })
            })

            chart.current?.clearData()
            chart.current?.applyNewData(data)
        }
        return () => {
            dispose('hades-klines-chart')
        }
    }, [bars, orders, positions]);
    const chart = useRef<Chart | null>(null);
    return <>
        <div id='hades-klines-chart' style={{ width: '90vw', height: '70vh', display: 'flex', justifyContent: 'center', alignContent: 'center' }} />
        <Radio.Group onChange={e => onIntervalChanged(e.target.value)} defaultValue="1m">
            <Radio.Button value="1m">1M</Radio.Button>
            <Radio.Button value="5m">5M</Radio.Button>
            <Radio.Button value="15m">15M</Radio.Button>
            <Radio.Button value="30m">30M</Radio.Button>
            <Radio.Button value="1h">1H</Radio.Button>
            <Radio.Button value="1d">1D</Radio.Button>
        </Radio.Group>
    </>

}