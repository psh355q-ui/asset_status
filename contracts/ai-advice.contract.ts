import { ApiResponse, PaginatedResponse } from './types';

// ------------- Schema ------------- //

export type Recommendation = 'BUY' | 'SELL' | 'HOLD';

export interface AIAdvice {
    id: string;
    user_id: string;
    symbol: string;
    recommendation: Recommendation;
    summary: string; // 3줄 요약
    details: Record<string, any>; // JSON data (news, macro, technical, etc.)
    confidence: number;
    created_at: string;
}

// ------------- API Contracts ------------- //

// POST /ai-advice/generate (Real-time generation or request)
export interface GenerateAdviceRequest {
    symbol: string;
}
export type GenerateAdviceResponse = ApiResponse<AIAdvice>;

// GET /ai-advice
export interface GetAdviceHistoryQuery {
    symbol?: string;
    recommendation?: Recommendation;
    page?: number;
    size?: number;
}
export type GetAdviceHistoryResponse = PaginatedResponse<AIAdvice>;

// GET /ai-advice/:id
export type GetAdviceDetailResponse = ApiResponse<AIAdvice>;
