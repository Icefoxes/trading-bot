export interface Order {
    orderId: number;
    orderType: string;
    symbol: string;
    instrumentType: string;
    price: number;
    status: string;
    side: string;
    quantity: number;
    timestamp: string;
}
