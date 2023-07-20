import { FC } from 'react';
import { Balance } from '../../models';
import { Table } from 'antd';
import type { ColumnsType } from 'antd/es/table';


export const BalanceComponent: FC<{ balances: Balance[] }> = ({ balances }) => {
    const columns: ColumnsType<Balance> = [
        {
            title: 'Asset',
            dataIndex: 'asset',
            key: 'asset',
        },
        {
            title: 'Available Balance',
            dataIndex: 'availableBalance',
            key: 'availableBalance',
        },
    ];

    return <Table dataSource={balances} columns={columns} />;
}