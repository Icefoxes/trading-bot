import { FC, useEffect, useState } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { ColDef, GridApi } from 'ag-grid-community';
import { Trade } from '../../models';
import './trade.component.scss';


export const TradeDetailComponent: FC<{ trades: Trade[] }> = ({ trades }) => {
    const columns: ColDef<Trade>[] = [
        {
            headerName: 'Order Id',
            field: 'orderId',
        },
        {
            headerName: 'Symbol',
            field: 'symbol'
        },
        {
            headerName: 'Price',
            field: 'price'
        },
        {
            headerName: 'Quantity',
            field: 'quantity',
        },
        {
            headerName: 'Side',
            field: 'side',
        },
        {
            headerName: 'Commission',
            field: 'commission'
        },
        {
            headerName: 'Commission Asset',
            field: 'commissionAsset',
        },
        {
            headerName: 'Commission To USDT',
            field: 'commissionToUSDT',
            valueFormatter: params => params.data?.commissionToUSDT?.toFixed(3) || ''
        },
        {
            headerName: 'Marker',
            field: 'maker',
        },
        {
            headerName: 'Realized PNL',
            field: 'realizedPnl',
            valueFormatter: params => params.data?.realizedPnl?.toFixed(3) || ''
        },
        {
            headerName: 'Datetime',
            field: 'timestamp',
            sortable: true
        }
    ];
    const [gridApi, setGridApi] = useState<GridApi<Trade> | null>(null);
    useEffect(() => {
        gridApi?.sizeColumnsToFit({
            defaultMinWidth: 50,
            columnLimits: [{ key: 'asset', minWidth: 100 }],
        });
    }, [gridApi])
    return <div className='commision-table-container'>
        <AgGridReact className="ag-theme-alpine" rowData={trades} columnDefs={columns} onGridReady={(e) => {
            setGridApi(e.api);
        }} />
    </div>;
}