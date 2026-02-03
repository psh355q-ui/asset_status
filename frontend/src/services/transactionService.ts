import { api } from './api';
import { ApiResponse } from './auth';

export type TransactionType = 'BUY' | 'SELL' | 'DIVIDEND' | 'DEPOSIT' | 'WITHDRAW';
export type Market = 'KR' | 'US';

export interface Transaction {
    id: string;
    account_id: string;
    symbol: string;
    market: Market;
    type: TransactionType;
    quantity: number;
    price: number;
    trade_date: string;
    created_at: string;
}

export interface TransactionCreateRequest {
    account_id: string;
    symbol: string;
    market: Market;
    type: TransactionType;
    quantity: number;
    price: number;
    trade_date: string;
}

export const transactionService = {
    createTransaction: async (data: TransactionCreateRequest): Promise<Transaction> => {
        const response = await api.post<ApiResponse<Transaction>>('/transactions', data);
        return response.data.data;
    },
    getTransactions: async (accountId?: string): Promise<Transaction[]> => {
        const url = accountId ? `/transactions?account_id=${accountId}` : '/transactions';
        const response = await api.get<ApiResponse<Transaction[]>>(url);
        return response.data.data;
    }
};
