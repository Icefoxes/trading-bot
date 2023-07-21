import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom';
import { MarketContainer, CommissionContainer } from '../features';
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
        ]
    },
]);

export const RootRouter = () => {
    return <RouterProvider router={router} />
}
