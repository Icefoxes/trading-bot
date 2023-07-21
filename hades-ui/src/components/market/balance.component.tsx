import { FC } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { ColDef } from 'ag-grid-community';

import { Balance } from '../../models';

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

    return <AgGridReact className="ag-theme-alpine" rowData={balances} columnDefs={columns} />;
}