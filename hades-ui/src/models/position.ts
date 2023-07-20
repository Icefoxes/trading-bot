export interface Position {
    symbol: string;
    instrumentType: string;
    side: string;
    quantity: number;
    unrealized_profit: number;
    unrealized_profit_ratio: number;
    mode: string;
    price: number;
    timestamp: Date;
}
