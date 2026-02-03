import React from 'react';
import { AIAdvice } from '../../services/aiAdviceService';
import './AIAdviceCard.css';

interface Props {
    advice: AIAdvice;
}

const AIAdviceCard: React.FC<Props> = ({ advice }) => {
    const getThemeClass = () => {
        switch (advice.recommendation) {
            case 'BUY': return 'advice-buy';
            case 'SELL': return 'advice-sell';
            case 'HOLD': return 'advice-hold';
            default: return '';
        }
    };

    const getRecommendationColor = () => {
        switch (advice.recommendation) {
            case 'BUY': return '#ff4d4d';
            case 'SELL': return '#4d94ff';
            case 'HOLD': return '#888';
            default: return '#fff';
        }
    };

    return (
        <div className={`advice-card ${getThemeClass()}`}>
            <div className="advice-header">
                <div className="advice-symbol">{advice.symbol}</div>
                <div
                    className="advice-recommendation"
                    style={{ color: getRecommendationColor() }}
                >
                    {advice.recommendation}
                </div>
            </div>

            <div className="advice-summary">{advice.summary}</div>

            <div className="advice-confidence">
                <span className="confidence-label">Confidence:</span>
                <span className="confidence-value">{Math.round(advice.confidence * 100)}%</span>
            </div>

            <details className="advice-details">
                <summary>View Details</summary>
                <div className="advice-details-content">{advice.details}</div>
            </details>

            <div className="advice-timestamp">
                {new Date(advice.created_at).toLocaleString('ko-KR')}
            </div>
        </div>
    );
};

export default AIAdviceCard;
