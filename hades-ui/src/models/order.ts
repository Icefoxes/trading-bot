export interface Order {
    orderId: string;
    orderType: string;
    symbol: string;
    instrumentType: string;
    price: number;
    status: string;
    side: string;
    quantity: number;
    timestamp: Date;
}
