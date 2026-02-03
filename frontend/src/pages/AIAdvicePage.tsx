import React, { useState, useEffect } from 'react';
import { aiAdviceService, AIAdvice } from '../services/aiAdviceService';
import AIAdviceCard from '../components/ai-advice/AIAdviceCard';
import './AIAdvicePage.css';

const AIAdvicePage: React.FC = () => {
    const [advices, setAdvices] = useState<AIAdvice[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [symbol, setSymbol] = useState('');
    const [isGenerating, setIsGenerating] = useState(false);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        setIsLoading(true);
        try {
            const data = await aiAdviceService.getHistory();
            setAdvices(data);
        } catch (error) {
            console.error('Failed to fetch advice history', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleGenerate = async () => {
        if (!symbol.trim()) return;

        setIsGenerating(true);
        try {
            const newAdvice = await aiAdviceService.generateAdvice(symbol);
            setAdvices([newAdvice, ...advices]);
            setSymbol('');
        } catch (error) {
            console.error('Failed to generate advice', error);
            alert('Failed to generate AI advice. Please try again.');
        } finally {
            setIsGenerating(false);
        }
    };

    return (
        <div className="ai-advice-page">
            <header className="page-header">
                <h1>AI Investment Advice</h1>
                <p className="disclaimer">
                    ⚠️ AI 조언은 참고용이며 투자 결정은 본인의 판단과 책임하에 이루어져야 합니다.
                </p>
            </header>

            <div className="advice-generator">
                <input
                    type="text"
                    placeholder="Enter stock symbol (e.g., 005930.KS, AAPL)"
                    value={symbol}
                    onChange={(e) => setSymbol(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleGenerate()}
                    className="symbol-input"
                />
                <button
                    onClick={handleGenerate}
                    disabled={isGenerating || !symbol.trim()}
                    className="generate-btn"
                >
                    {isGenerating ? 'Generating...' : 'Get AI Advice'}
                </button>
            </div>

            <div className="advice-history">
                <h2>Advice History</h2>
                {isLoading ? (
                    <div className="loading">Loading history...</div>
                ) : advices.length === 0 ? (
                    <div className="empty-state">No advice history yet. Generate your first advice!</div>
                ) : (
                    advices.map((advice) => (
                        <AIAdviceCard key={advice.id} advice={advice} />
                    ))
                )}
            </div>
        </div>
    );
};

export default AIAdvicePage;
