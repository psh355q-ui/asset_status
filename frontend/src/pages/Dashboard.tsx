import { useEffect, useState } from 'react';
import { useAuthStore } from '../store/useAuthStore';
import { useAccountStore } from '../store/useAccountStore';
import { useNavigate } from 'react-router-dom';
import AccountCard from '../components/accounts/AccountCard';
import CreateAccountModal from '../components/accounts/CreateAccountModal';
import TransactionFormModal from '../components/transactions/TransactionFormModal';
import { Plus, LogOut, DollarSign } from 'lucide-react';
import './Dashboard.css';

const Dashboard = () => {
    const { user, logout } = useAuthStore();
    const { accounts, fetchAccounts, isLoading } = useAccountStore();
    const navigate = useNavigate();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isTransactionModalOpen, setIsTransactionModalOpen] = useState(false);

    useEffect(() => {
        fetchAccounts();
    }, [fetchAccounts]);

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <div>
                    <h1 className="dashboard-title">Asset Overview</h1>
                    <p style={{ color: '#888' }}>Welcome back, {user?.email}</p>
                </div>
                <div style={{ display: 'flex', gap: '1rem', width: 'auto' }}>
                    <button
                        onClick={() => setIsModalOpen(true)}
                        className="btn btn-primary"
                        style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
                    >
                        <Plus size={20} />
                        Add Account
                    </button>
                    <button
                        onClick={() => setIsTransactionModalOpen(true)}
                        className="btn btn-secondary"
                        style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(255,255,255,0.1)', color: 'white' }}
                    >
                        <DollarSign size={20} />
                        Add Transaction
                    </button>
                    <button onClick={handleLogout} className="btn btn-secondary">
                        <LogOut size={20} />
                    </button>
                </div>
            </header>

            <main>
                {isLoading && accounts.length === 0 ? (
                    <div style={{ textAlign: 'center', marginTop: '2rem' }}>Loading accounts...</div>
                ) : (
                    <>
                        {accounts.length === 0 ? (
                            <div className="empty-state">
                                <p>No accounts found.</p>
                                <p style={{ marginTop: '0.5rem' }}>Create your first account to get started!</p>
                                <button
                                    onClick={() => setIsModalOpen(true)}
                                    className="btn btn-primary"
                                    style={{ marginTop: '1rem' }}
                                >
                                    Create Account
                                </button>
                            </div>
                        ) : (
                            <div className="accounts-grid">
                                {accounts.map(account => (
                                    <AccountCard key={account.id} account={account} />
                                ))}
                            </div>
                        )}
                    </>
                )}
            </main>

            <CreateAccountModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
            <TransactionFormModal isOpen={isTransactionModalOpen} onClose={() => setIsTransactionModalOpen(false)} />
        </div>
    );
};

export default Dashboard;
