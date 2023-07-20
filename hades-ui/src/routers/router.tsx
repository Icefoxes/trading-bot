import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { MarketContainer, AuthContainer } from '../features';
import { BasicLayout } from './layout';

const router = createBrowserRouter([
    {
        path: '/',
        element: <BasicLayout />,
        children: [
            {
                path: '/klines/:interval',
                element: <MarketContainer />
            },
            {
                path: '/auth',
                element: <AuthContainer />
            },
        ]
    },
], { basename: '/web' });

export const RootRouter = () => {
    return <RouterProvider router={router} />
}
