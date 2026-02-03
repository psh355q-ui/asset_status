import { ApiResponse, PaginatedResponse } from './types';

// ------------- Schema ------------- //

export type Market = 'KR' | 'US';
export type TransactionType = 'BUY' | 'SELL';

export interface Transaction {
    id: string;
    user_id: string;
    account_id: string;
    symbol: string;
    market: Market;
    type: TransactionType;
    quantity: number;
    price: number;
    trade_date: string; // YYYY-MM-DD
    created_at: string;
}

// ------------- API Contracts ------------- //

// POST /transactions
export interface CreateTransactionRequest {
    account_id: string;
    symbol: string;
    market: Market;
    type: TransactionType;
    quantity: number;
    price: number;
    trade_date: string;
}
export type CreateTransactionResponse = ApiResponse<Transaction>;

// GET /transactions
export interface GetTransactionsQuery {
    account_id?: string;
    symbol?: string;
    start_date?: string;
    end_date?: string;
    page?: number;
    size?: number;
}
export type GetTransactionsResponse = PaginatedResponse<Transaction>;
