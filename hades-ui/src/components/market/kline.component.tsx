import { useRef, useEffect, FC } from 'react';
import { init } from 'klinecharts';
import { Kline } from '../../models';
import moment from 'moment';

export const KLineComponent: FC<{ bars: Kline[] }> = ({ bars }) => {
    useEffect(() => {
        if (bars.length > 0) {
            document.title = `${bars[0]?.close}`;
        }
    }, [bars]);
    useEffect(() => {
        if (ref.current) {
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
                const chart = init(ref.current);
                chart?.clearData()
                chart?.applyNewData(data.reverse())
            }
        }
    }, [bars]);
    const ref = useRef<HTMLDivElement>(null);
    return <div ref={ref} style={{ width: '90vw', height: '80vh', display: 'flex', justifyContent: 'center', alignContent: 'center' }}>
    </div>
}