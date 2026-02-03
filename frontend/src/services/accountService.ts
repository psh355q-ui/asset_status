import { api } from './api';
import { ApiResponse } from './auth';

export type AccountType = 'ISA' | 'PENSION' | 'GENERAL' | 'OVERSEAS' | 'GOLD';

export interface Account {
    id: string;
    user_id: string;
    account_type: AccountType;
    name: string;
    created_at: string;
    updated_at?: string;
}

export interface AccountCreateRequest {
    name: string;
    account_type: AccountType;
}

export const accountService = {
    getAccounts: async (): Promise<Account[]> => {
        const response = await api.get<ApiResponse<Account[]>>('/accounts');
        return response.data.data;
    },
    createAccount: async (data: AccountCreateRequest): Promise<Account> => {
        const response = await api.post<ApiResponse<Account>>('/accounts', data);
        return response.data.data;
    },
    deleteAccount: async (id: string): Promise<void> => {
        await api.delete(`/accounts/${id}`);
    }
};
