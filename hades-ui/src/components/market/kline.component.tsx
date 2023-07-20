import { useRef, useEffect, FC } from 'react';
import { Chart, init, dispose } from 'klinecharts';
import { Kline } from '../../models';
import moment from 'moment';

export const KLineComponent: FC<{ bars: Kline[] }> = ({ bars }) => {
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
            }
        });
        if (data.length > 0) {
            chart.current = init('hades-klines-chart');
            chart.current?.clearData()
            chart.current?.applyNewData(data)
        }
        return () => {
            dispose('hades-klines-chart')
        }
    }, [bars]);
    const chart = useRef<Chart | null>(null);
    return <div id='hades-klines-chart' style={{ width: '90vw', height: '70vh', display: 'flex', justifyContent: 'center', alignContent: 'center' }} />
    
}