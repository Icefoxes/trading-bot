import { FC, useEffect, useRef } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { ColDef } from 'ag-grid-community';
import { Order } from '../../models';
import './account.component.scss'


export const OrderComponent: FC<{ orders: Order[] }> = ({ orders }) => {
    const gridRef = useRef<AgGridReact | null>(null);
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
    useEffect(() => {
        gridRef?.current?.api.sizeColumnsToFit();
    }, [])
    return <div className='table-container'>
        <AgGridReact ref={gridRef} className="ag-theme-alpine" rowData={orders} columnDefs={columns} />
    </div>;
}