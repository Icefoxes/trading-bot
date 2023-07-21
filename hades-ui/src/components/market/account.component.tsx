import { FC } from 'react';
import { Tabs } from 'antd';

import { OrderComponent } from './order.component';
import { PositionComponent } from './position.component';
import { BalanceComponent } from './balance.component';
import { Order, Position, Balance } from '../../models';

import './account.component.scss'

export const AccountComponent: FC<{ orders: Order[], positions: Position[], balances: Balance[] }> = ({ orders, positions, balances }) => {
    return <Tabs className='account-tabs' items={[
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
        {
            key: '3',
            label: `Balance`,
            children: <BalanceComponent balances={balances} />,
        },
    ]}>
    </Tabs >
}