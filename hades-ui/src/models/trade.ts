export interface Trade {
    symbol: string;
    id: string;
    orderId: string;
    side: string;
    price: number;
    quantity: number;
    realizedPnl: number;
    marginAsset: string;
    quoteQty: number;
    commission: number;
    commissionToUSDT: number;
    commissionAsset: string;
    timestamp: Date;
    maker: boolean;
}
