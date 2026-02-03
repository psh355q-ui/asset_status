
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import TransactionFormModal from '../../components/transactions/TransactionFormModal';
import { accountService } from '../../services/accountService';

// Mock Services
vi.mock('../../services/accountService', () => ({
    accountService: {
        getAccounts: vi.fn()
    }
}));

vi.mock('../../store/useAccountStore', () => ({
    useAccountStore: () => ({
        accounts: [
            { id: 'acc1', name: 'My Account', account_type: 'GENERAL' }
        ],
        fetchAccounts: vi.fn()
    })
}));

describe('TransactionFormModal', () => {
    it('renders form fields correctly', () => {
        render(<TransactionFormModal isOpen={true} onClose={() => { }} />);

        expect(screen.getByText('Add Transaction')).toBeInTheDocument();
        expect(screen.getByLabelText('Account')).toBeInTheDocument();
        expect(screen.getByLabelText('Symbol')).toBeInTheDocument();
        expect(screen.getByLabelText('Quantity')).toBeInTheDocument();
        expect(screen.getByLabelText('Price')).toBeInTheDocument();
    });

    it('validates required fields', async () => {
        render(<TransactionFormModal isOpen={true} onClose={() => { }} />);

        const submitBtn = screen.getByText('Submit');
        fireEvent.click(submitBtn);

        await waitFor(() => {
            expect(screen.getByText('Symbol is required')).toBeInTheDocument();
        });
    });
});
