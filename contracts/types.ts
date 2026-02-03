export interface Request<T = any> {
    data: T;
}

export interface ApiResponse<T = any> {
    data: T;
    meta?: {
        total?: number;
        page?: number;
        last_page?: number;
    };
    message?: string;
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
    meta: {
        total: number;
        page: number;
        last_page: number;
    };
}
