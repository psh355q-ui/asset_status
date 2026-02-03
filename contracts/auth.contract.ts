import { ApiResponse } from './types';

// ------------- Schema ------------- //

export interface User {
    id: string;
    email: string;
    created_at: string;
    updated_at: string;
}

export interface AuthToken {
    access_token: string;
    token_type: string;
}

// ------------- API Contracts ------------- //

// POST /auth/register
export interface RegisterRequest {
    email: string;
    password: string;
}
export type RegisterResponse = ApiResponse<User>;

// POST /auth/login
export interface LoginRequest {
    username: string; // OAuth2 standard uses username field for email
    password: string;
}
export type LoginResponse = AuthToken;

// GET /auth/me
export type MeResponse = ApiResponse<User>;
