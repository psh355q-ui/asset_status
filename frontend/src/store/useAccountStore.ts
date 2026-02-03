import { create } from 'zustand';
import { Account, accountService, AccountCreateRequest } from '../services/accountService';

interface AccountState {
    accounts: Account[];
    isLoading: boolean;
    error: string | null;
    fetchAccounts: () => Promise<void>;
    createAccount: (data: AccountCreateRequest) => Promise<void>;
    deleteAccount: (id: string) => Promise<void>;
}

export const useAccountStore = create<AccountState>((set, get) => ({
    accounts: [],
    isLoading: false,
    error: null,

    fetchAccounts: async () => {
        set({ isLoading: true, error: null });
        try {
            const accounts = await accountService.getAccounts();
            set({ accounts, isLoading: false });
        } catch (error: any) {
            set({ isLoading: false, error: error.message || 'Failed to fetch accounts' });
        }
    },

    createAccount: async (data: AccountCreateRequest) => {
        set({ isLoading: true, error: null });
        try {
            await accountService.createAccount(data);
            // Refresh list
            await get().fetchAccounts();
        } catch (error: any) {
            set({ isLoading: false, error: error.message || 'Failed to create account' });
            throw error; // Let UI handle success/redirect
        }
    },

    deleteAccount: async (id: string) => {
        set({ isLoading: true, error: null });
        try {
            await accountService.deleteAccount(id);
            // Refresh list
            await get().fetchAccounts();
        } catch (error: any) {
            set({ isLoading: false, error: error.message || 'Failed to delete account' });
        }
    }
}));
