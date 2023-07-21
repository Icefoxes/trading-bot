import { FC, useEffect, useRef } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { ColDef } from 'ag-grid-community';
import { Balance } from '../../models';
import './account.component.scss'


export const BalanceComponent: FC<{ balances: Balance[] }> = ({ balances }) => {
    const gridRef = useRef<AgGridReact | null>(null);
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
    useEffect(() => {
        gridRef?.current?.api.sizeColumnsToFit();
    }, [])
    return <div className='table-container'>
        <AgGridReact ref={gridRef} className="ag-theme-alpine" rowData={balances} columnDefs={columns} />
    </div>;
}