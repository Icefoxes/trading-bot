import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { MarketContainer } from "../features";

const router = createBrowserRouter([
    {
        path: "/",
        element: <MarketContainer />
    },
]);

export const RootRouter = () => {
    return <RouterProvider router={router} />
}
