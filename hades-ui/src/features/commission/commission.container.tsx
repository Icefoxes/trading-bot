import { useGetTradesQuery } from "../../services"

export const CommissionContainer = () => {
    const { data: trades } = useGetTradesQuery({ symbol: 'BTCUSDT' });
    return <>
    </>
}