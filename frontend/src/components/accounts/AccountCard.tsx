import React from 'react';
import { Account } from '../../services/accountService';
import './AccountCard.css';
import { Wallet } from 'lucide-react';

interface Props {
    account: Account;
}

const AccountCard: React.FC<Props> = ({ account }) => {
    return (
        <div className="account-card">
            <div className="account-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Wallet size={20} className="text-gray-400" />
                    <span className="account-name">{account.name}</span>
                </div>
                <span className="account-type">{account.account_type}</span>
            </div>
            {/* Balance placeholder - Will be implemented in Phase 3 */}
            <div style={{ marginTop: '1rem', fontSize: '1.5rem', fontWeight: 'bold' }}>
                ₩0
            </div>
            <div style={{ fontSize: '0.8rem', color: '#888' }}>
                Num: {account.id.substring(0, 8)}...
            </div>
        </div>
    );
};

export default AccountCard;
