import { FC } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { ColDef } from 'ag-grid-community';
import { Order } from '../../models';



export const OrderComponent: FC<{ orders: Order[] }> = ({ orders }) => {
    const columns: ColDef<Order>[] = [
        {
            headerName: 'Symbol',
            field: 'symbol',

        },
        {
            headerName: 'Side',
            field: 'side',

        },
        {
            headerName: 'Size',
            field: 'quantity',

        },
        {
            headerName: 'Entry Price',
            field: 'price',

        },
        {
            headerName: 'Order Id',
            field: 'orderId',

        },
        {
            headerName: 'Order Type',
            field: 'orderType',

        }
    ];

    return <AgGridReact className="ag-theme-alpine" rowData={orders} columnDefs={columns} />;
}