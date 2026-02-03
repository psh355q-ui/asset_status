import { ApiResponse, PaginatedResponse } from './types';

// ------------- Schema ------------- //

export type AccountType = 'ISA' | 'PENSION' | 'GENERAL' | 'OVERSEAS' | 'GOLD';

export interface Account {
    id: string;
    user_id: string;
    account_type: AccountType;
    name: string;
    created_at: string;
    updated_at: string;
}

// ------------- API Contracts ------------- //

// POST /accounts
export interface CreateAccountRequest {
    account_type: AccountType;
    name: string;
}
export type CreateAccountResponse = ApiResponse<Account>;

// GET /accounts
export type GetAccountsResponse = ApiResponse<Account[]>; // Not paginated usually, but can be

// GET /accounts/:id
export type GetAccountResponse = ApiResponse<Account>;

// PUT /accounts/:id
export interface UpdateAccountRequest {
    name: string;
}
export type UpdateAccountResponse = ApiResponse<Account>;

// DELETE /accounts/:id
export type DeleteAccountResponse = ApiResponse<{ id: string }>;
