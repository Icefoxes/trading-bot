import { FC } from 'react';

import { EditorComponent } from '../../components';
import './backtesting.container.scss';

export const BacktestingContainer: FC<{}> = () => {
    return <div className='backtesting-container'>
        <EditorComponent />
    </div>
}