import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useAccountStore } from '../../store/useAccountStore';
import { AccountType } from '../../services/accountService';
import './CreateAccountModal.css';
import { X } from 'lucide-react';

const schema = z.object({
    name: z.string().min(1, "Account name is required"),
    account_type: z.enum(['ISA', 'PENSION', 'GENERAL', 'OVERSEAS', 'GOLD'] as const)
});

type FormData = z.infer<typeof schema>;

interface Props {
    isOpen: boolean;
    onClose: () => void;
}

const CreateAccountModal: React.FC<Props> = ({ isOpen, onClose }) => {
    const { createAccount, isLoading } = useAccountStore();
    const { register, handleSubmit, formState: { errors }, reset } = useForm<FormData>({
        resolver: zodResolver(schema),
        defaultValues: { account_type: 'GENERAL' }
    });

    if (!isOpen) return null;

    const onSubmit = async (data: FormData) => {
        try {
            await createAccount(data);
            reset();
            onClose();
        } catch (err) {
            // Error handling handled by store/UI toast ideally
        }
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
                    <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>Add New Account</h2>
                    <button onClick={onClose} style={{ background: 'none', border: 'none', color: '#888', cursor: 'pointer' }}>
                        <X size={24} />
                    </button>
                </div>

                <form onSubmit={handleSubmit(onSubmit)}>
                    <div className="form-group">
                        <label className="form-label">Account Name</label>
                        <input
                            {...register('name')}
                            className="form-input"
                            placeholder="e.g. Broken Piggy Bank"
                            autoFocus
                        />
                        {errors.name && <span className="error-text">{errors.name.message}</span>}
                    </div>

                    <div className="form-group">
                        <label className="form-label">Account Type</label>
                        <select {...register('account_type')} className="form-select">
                            <option value="GENERAL">General Investment</option>
                            <option value="ISA">ISA (Tax-Free)</option>
                            <option value="PENSION">Pension / IRP</option>
                            <option value="OVERSEAS">Overseas Stock</option>
                            <option value="GOLD">Gold / Commodity</option>
                        </select>
                        {errors.account_type && <span className="error-text">{errors.account_type.message}</span>}
                    </div>

                    <div className="modal-actions">
                        <button type="button" onClick={onClose} className="btn btn-secondary">Cancel</button>
                        <button type="submit" className="btn btn-primary" disabled={isLoading}>
                            {isLoading ? 'Creating...' : 'Create Account'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default CreateAccountModal;
