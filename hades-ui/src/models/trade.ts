export interface Trade {
    symbol: string;
    id: number;
    orderId: number;
    side: string;
    price: number;
    quantity: number;
    realizedPnl: number;
    marginAsset: string;
    quoteQty: number;
    commission: number;
    commissionToUSDT: number;
    commissionAsset: string;
    timestamp: string;
    maker: boolean;
}
