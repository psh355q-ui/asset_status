import { api } from './api';
import { ApiResponse } from './auth';

export interface AIAdvice {
    id: string;
    user_id: string;
    symbol: string;
    recommendation: 'BUY' | 'SELL' | 'HOLD';
    summary: string;
    details: string;
    confidence: number;
    created_at: string;
}

export const aiAdviceService = {
    generateAdvice: async (symbol: string): Promise<AIAdvice> => {
        const response = await api.post<ApiResponse<AIAdvice>>('/ai-advice/generate', { symbol });
        return response.data.data;
    },

    getHistory: async (): Promise<AIAdvice[]> => {
        const response = await api.get<ApiResponse<AIAdvice[]>>('/ai-advice/history');
        return response.data.data;
    }
};
