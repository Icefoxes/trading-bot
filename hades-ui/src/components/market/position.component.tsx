import { FC } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { ColDef } from 'ag-grid-community';
import { Position } from '../../models';

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

    return <AgGridReact className="ag-theme-alpine" rowData={positions} columnDefs={columns} />;
}