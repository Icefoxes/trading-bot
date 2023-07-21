import { FC, useEffect, useState } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { ColDef, GridApi } from 'ag-grid-community';
import { Position } from '../../models';
import './account.component.scss'

export const PositionComponent: FC<{ positions: Position[] }> = ({ positions }) => {
    const columns: ColDef<Position>[] = [
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
            valueFormatter: params => params.data?.price?.toFixed(3) || ''
        },
        {
            headerName: 'Unrealized Profit',
            field: 'unrealized_profit',

        },
        {
            headerName: 'Unrealized Profit Ratio',
            field: 'unrealized_profit_ratio',

        },
        {
            headerName: 'Mode',
            field: 'mode',

        }
    ];
    const [gridApi, setGridApi] = useState<GridApi<Position> | null>(null);
    useEffect(() => {
        gridApi?.sizeColumnsToFit({
            defaultMinWidth: 20,
        });
    }, [gridApi])
    return <div className='table-container'>
        <AgGridReact className="ag-theme-alpine" rowData={positions} columnDefs={columns} onGridReady={(e) => {
            setGridApi(e.api);
        }} />
    </div>;
}