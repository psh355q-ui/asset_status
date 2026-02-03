import { api } from './api';

// --- Types (Mirrors Backend Contracts) ---

export interface User {
    id: string;
    email: string;
    created_at?: string;
}

export interface AuthToken {
    access_token: string;
    token_type: string;
}

export interface ApiResponse<T> {
    data: T;
    message?: string;
}

// REQUEST Types
export interface LoginRequest {
    email: string; // UI uses email, mapped to username
    password: string;
}

export interface RegisterRequest {
    email: string;
    password: string;
}

// RESPONSE Types
export type LoginResponse = AuthToken;
export type RegisterResponse = ApiResponse<User>;

// --- Service ---

export const authService = {
    // POST /api/auth/register
    register: async (data: RegisterRequest): Promise<User> => {
        const response = await api.post<RegisterResponse>('/auth/register', data);
        // Backend returns { data: User }
        return response.data.data;
    },

    // POST /api/auth/login
    login: async (data: LoginRequest): Promise<AuthToken> => {
        // Backend expects 'username' (OAuth2 standard)
        const payload = {
            username: data.email,
            password: data.password
        };
        const response = await api.post<LoginResponse>('/auth/login', payload);
        // Backend returns token directly (no data wrapper)
        return response.data;
    },

    // GET /api/auth/health or me (Optional verification)
    // For now, no /me endpoint implemented yet in T1.1 (Wait, T1.1 implemented only register/login)
    // We will assume login is enough.
};
