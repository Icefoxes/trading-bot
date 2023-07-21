import { FC, useEffect, useRef } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { ColDef } from 'ag-grid-community';
import { Position } from '../../models';
import './account.component.scss'

export const PositionComponent: FC<{ positions: Position[] }> = ({ positions }) => {
    const gridRef = useRef<AgGridReact | null>(null);
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
    useEffect(() => {
        gridRef?.current?.api.sizeColumnsToFit();
    }, [])
    return <div className='table-container'>
        <AgGridReact ref={gridRef} className="ag-theme-alpine" rowData={positions} columnDefs={columns} />
    </div>;
}