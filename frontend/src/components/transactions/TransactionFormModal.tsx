import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { X } from 'lucide-react';
import { useAccountStore } from '../../store/useAccountStore';
import { transactionService, TransactionCreateRequest } from '../../services/transactionService';
import './TransactionFormModal.css';

const schema = z.object({
    account_id: z.string().min(1, "Account is required"),
    market: z.enum(['KR', 'US']),
    type: z.enum(['BUY', 'SELL', 'DIVIDEND', 'DEPOSIT', 'WITHDRAW']),
    symbol: z.string().min(1, "Symbol is required"),
    quantity: z.number().min(0.0001, "Quantity must be positive"),
    price: z.number().min(0, "Price must be positive"), // 0 allowed for free? usually >0
    trade_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Invalid date format")
});

type FormData = z.infer<typeof schema>;

interface Props {
    isOpen: boolean;
    onClose: () => void;
    onSuccess?: () => void;
}

const TransactionFormModal: React.FC<Props> = ({ isOpen, onClose, onSuccess }) => {
    const { accounts, fetchAccounts } = useAccountStore();
    const { register, handleSubmit, formState: { errors }, reset } = useForm<FormData>({
        resolver: zodResolver(schema),
        defaultValues: {
            market: 'KR',
            type: 'BUY',
            trade_date: new Date().toISOString().split('T')[0],
            quantity: 0,
            price: 0
        }
    });

    useEffect(() => {
        if (isOpen && accounts.length === 0) {
            fetchAccounts();
        }
    }, [isOpen, accounts.length, fetchAccounts]);

    if (!isOpen) return null;

    const onSubmit = async (data: FormData) => {
        try {
            await transactionService.createTransaction(data);
            reset();
            onSuccess && onSuccess();
            onClose();
        } catch (error) {
            console.error('Failed to create transaction', error);
            // TODO: Toast error
        }
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
                <div className="modal-header">
                    <h2 className="modal-title">Add Transaction</h2>
                    <button onClick={onClose} className="close-btn"><X size={20} /></button>
                </div>

                <form onSubmit={handleSubmit(onSubmit)}>
                    <div className="form-group">
                        <label className="form-label" htmlFor="account_id">Account</label>
                        <select id="account_id" {...register('account_id')} className="form-select">
                            <option value="">Select Account</option>
                            {accounts.map(acc => (
                                <option key={acc.id} value={acc.id}>{acc.name} ({acc.account_type})</option>
                            ))}
                        </select>
                        {errors.account_id && <span className="error-text">{errors.account_id.message}</span>}
                    </div>

                    <div style={{ display: 'flex', gap: '12px' }}>
                        <div className="form-group" style={{ flex: 1 }}>
                            <label className="form-label">Market</label>
                            <select {...register('market')} className="form-select">
                                <option value="KR">KR (Domestic)</option>
                                <option value="US">US (Overseas)</option>
                            </select>
                        </div>
                        <div className="form-group" style={{ flex: 1 }}>
                            <label className="form-label">Type</label>
                            <select {...register('type')} className="form-select">
                                <option value="BUY">Buy</option>
                                <option value="SELL">Sell</option>
                                <option value="DIVIDEND">Dividend</option>
                                <option value="DEPOSIT">Deposit</option>
                                <option value="WITHDRAW">Withdraw</option>
                            </select>
                        </div>
                    </div>

                    <div className="form-group">
                        <label className="form-label" htmlFor="symbol">Symbol</label>
                        <input
                            id="symbol"
                            {...register('symbol')}
                            className="form-input"
                            placeholder="e.g. 005930 or AAPL"
                        />
                        {errors.symbol && <span className="error-text">{errors.symbol.message}</span>}
                    </div>

                    <div style={{ display: 'flex', gap: '12px' }}>
                        <div className="form-group" style={{ flex: 1 }}>
                            <label className="form-label" htmlFor="quantity">Quantity</label>
                            <input
                                id="quantity"
                                type="number"
                                step="any"
                                {...register('quantity', { valueAsNumber: true })}
                                className="form-input"
                            />
                            {errors.quantity && <span className="error-text">{errors.quantity.message}</span>}
                        </div>
                        <div className="form-group" style={{ flex: 1 }}>
                            <label className="form-label" htmlFor="price">Price</label>
                            <input
                                id="price"
                                type="number"
                                step="any"
                                {...register('price', { valueAsNumber: true })}
                                className="form-input"
                            />
                            {errors.price && <span className="error-text">{errors.price.message}</span>}
                        </div>
                    </div>

                    <div className="form-group">
                        <label className="form-label">Date</label>
                        <input
                            type="date"
                            {...register('trade_date')}
                            className="form-input"
                        />
                        {errors.trade_date && <span className="error-text">{errors.trade_date.message}</span>}
                    </div>

                    <div className="modal-actions">
                        <button type="button" onClick={onClose} className="btn" style={{ background: 'transparent', color: '#ccc', border: '1px solid rgba(255,255,255,0.1)' }}>Cancel</button>
                        <button type="submit" className="btn btn-primary">Submit</button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default TransactionFormModal;
