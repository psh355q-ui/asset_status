import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import AIAdviceCard from '../../components/ai-advice/AIAdviceCard';

const mockAdvice = {
    id: '1',
    user_id: 'user-1',
    symbol: '005930.KS',
    recommendation: 'BUY' as const,
    summary: 'Strong buy signal based on fundamentals',
    details: 'Samsung Electronics shows strong performance with semiconductor recovery...',
    confidence: 0.85,
    created_at: new Date().toISOString()
};

describe('AIAdviceCard', () => {
    it('renders recommendation correctly', () => {
        render(<AIAdviceCard advice={mockAdvice} />);

        expect(screen.getByText('BUY')).toBeInTheDocument();
        expect(screen.getByText('005930.KS')).toBeInTheDocument();
        expect(screen.getByText('Strong buy signal based on fundamentals')).toBeInTheDocument();
    });

    it('displays confidence level', () => {
        render(<AIAdviceCard advice={mockAdvice} />);
        expect(screen.getByText('85%')).toBeInTheDocument();
    });

    it('applies correct theme for BUY recommendation', () => {
        const { container } = render(<AIAdviceCard advice={mockAdvice} />);
        const card = container.querySelector('.advice-card');
        expect(card).toHaveClass('advice-buy');
    });

    it('applies correct theme for SELL recommendation', () => {
        const sellAdvice = { ...mockAdvice, recommendation: 'SELL' as const };
        const { container } = render(<AIAdviceCard advice={sellAdvice} />);
        const card = container.querySelector('.advice-card');
        expect(card).toHaveClass('advice-sell');
    });
});
