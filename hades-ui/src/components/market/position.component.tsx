import { FC } from 'react';
import { Position } from '../../models';
import { Table } from 'antd';
import type { ColumnsType } from 'antd/es/table';


export const PositionComponent: FC<{ positions: Position[] }> = ({ positions }) => {
    const columns: ColumnsType<Position> = [
        {
            title: 'Symbol',
            dataIndex: 'symbol',
            key: 'symbol',
        },
        {
            title: 'Side',
            dataIndex: 'side',
            key: 'side',
        },
        {
            title: 'Size',
            dataIndex: 'quantity',
            key: 'quantity',
        },
        {
            title: 'Unrealized Profit',
            dataIndex: 'unrealized_profit',
            key: 'unrealized_profit',
        },

        {
            title: 'Unrealized Profit Ratio',
            dataIndex: 'pnl_ratio',
            key: 'pnl_ratio',
        },
        {
            title: 'Mode',
            dataIndex: 'mode',
            key: 'mode',
        }
    ];

    return <Table dataSource={positions} columns={columns} />;
}