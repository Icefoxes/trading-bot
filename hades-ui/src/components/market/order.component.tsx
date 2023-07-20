import { FC } from 'react';
import { Order } from '../../models';
import { Table } from 'antd';
import type { ColumnsType } from 'antd/es/table';


export const OrderComponent: FC<{ orders: Order[] }> = ({ orders }) => {
    const columns: ColumnsType<Order> = [
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
            title: 'Entry Price',
            dataIndex: 'price',
            key: 'price',
        },

        {
            title: 'Order Id',
            dataIndex: 'orderId',
            key: 'orderId',
        },
        {
            title: 'Order Type',
            dataIndex: 'orderType',
            key: 'orderType',
        }
    ];

    return <Table dataSource={orders} columns={columns} />;
}