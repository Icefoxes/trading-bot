import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom';
import { MarketContainer, CommissionContainer, BacktestingContainer } from '../features';
import { BasicLayout } from './layout';

const router = createBrowserRouter([
    {
        path: '/',
        element: <BasicLayout />,
        children: [
            { index: true, element: <Navigate to="/market" replace /> },
            {
                path: '/market',
                element: <MarketContainer />,
                index: true
            },
            {
                path: 'commission',
                element: <CommissionContainer />,
            },
            {
                path: 'backtesting',
                element: <BacktestingContainer />,
            }
        ]
    },
]);

export const RootRouter = () => {
    return <RouterProvider router={router} />
}
