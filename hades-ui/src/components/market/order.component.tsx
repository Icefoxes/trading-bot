import { FC, useEffect, useState } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { ColDef, GridApi } from 'ag-grid-community';
import { Order } from '../../models';
import './account.component.scss'


export const OrderComponent: FC<{ orders: Order[] }> = ({ orders }) => {
    const columns: ColDef<Order>[] = [
        {
            headerName: 'Order Id',
            field: 'orderId',

        },
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
            headerName: 'Price',
            field: 'price',

        },   
        {
            headerName: 'Order Type',
            field: 'orderType',
        }
    ];
    const [gridApi, setGridApi] = useState<GridApi<Order> | null>(null);
    useEffect(() => {
        gridApi?.sizeColumnsToFit({
            defaultMinWidth: 50,
            columnLimits: [{ key: 'asset', minWidth: 100 }],
        });
    }, [gridApi])
    return <div className='table-container'>
        <AgGridReact className="ag-theme-alpine" rowData={orders} columnDefs={columns} onGridReady={(e) => {
            setGridApi(e.api);
        }} />
    </div>;
}