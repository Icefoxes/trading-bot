import { FC } from 'react';
import { Tabs } from 'antd';

import { OrderComponent } from './order.component';
import { PositionComponent } from './position.component';
import { Order, Position } from '../../models';


export const AccountComponent: FC<{ orders: Order[], positions: Position[] }> = ({ orders, positions }) => {
    return <Tabs items={[
        {
            key: '1',
            label: `Positions`,
            children: <PositionComponent positions={positions} />,
        },
        {
            key: '2',
            label: `Orders`,
            children: <OrderComponent orders={orders} />,
        },
    ]}>
    </Tabs >
}