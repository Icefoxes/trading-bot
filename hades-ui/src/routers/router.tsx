import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { MarketContainer } from '../features';
import { BasicLayout } from './layout';

const router = createBrowserRouter([
    {
        path: '/',
        element: <BasicLayout />,
        children: [
            {
                path: '/klines/:interval',
                element: <MarketContainer />,
                index: true
            },
        ]
    },
]);

export const RootRouter = () => {
    return <RouterProvider router={router} />
}
