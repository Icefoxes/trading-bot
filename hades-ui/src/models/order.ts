export interface Order {
    orderId: string;
    orderType: string;
    symbol: string;
    instrumentType: string;
    price: number;
    mode: string;
    status: string;
    side: string;
    lever: number;
    qty: number;
    timestamp: Date;
}
