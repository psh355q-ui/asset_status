
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import AccountCard from '../../components/accounts/AccountCard';
import { Account } from '../../services/accountService';

const mockAccount: Account = {
    id: '123',
    user_id: 'user1',
    name: '내 월급통장',
    account_type: 'GENERAL',
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z'
};

describe('AccountCard', () => {
    it('renders account information correctly', () => {
        render(<AccountCard account={mockAccount} />);

        expect(screen.getByText('내 월급통장')).toBeInTheDocument();
        expect(screen.getByText('GENERAL')).toBeInTheDocument();
        // 잔액이 없어도 0원으로 표시되어야 함 (Optional requirement)
    });
});
