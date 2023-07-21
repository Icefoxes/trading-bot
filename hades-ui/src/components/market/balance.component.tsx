import { FC, useEffect, useState } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { ColDef, GridApi } from 'ag-grid-community';
import { Balance } from '../../models';
import './account.component.scss'


export const BalanceComponent: FC<{ balances: Balance[] }> = ({ balances }) => {
    const columns: ColDef<Balance>[] = [
        {
            headerName: 'Asset',
            field: 'asset',
        },
        {
            headerName: 'Available Balance',
            field: 'availableBalance',
        },
    ];
    const [gridApi, setGridApi] = useState<GridApi<Balance> | null>(null);
    useEffect(() => {
        gridApi?.sizeColumnsToFit({
            defaultMinWidth: 50,
            columnLimits: [{ key: 'asset', minWidth: 100 }],
        });
    }, [gridApi])
    return <div className='table-container'>
        <AgGridReact className="ag-theme-alpine" rowData={balances} columnDefs={columns} onGridReady={(e) => {
            setGridApi(e.api);
        }} />
    </div>;
}