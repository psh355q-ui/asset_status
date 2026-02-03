import { http, HttpResponse } from 'msw'

export const handlers = [
    http.get('/api/health', () => {
        return HttpResponse.json({ status: 'healthy (mock)' })
    }),

    // Auth Mocks (Phase 1 placeholder)
    http.post('/api/auth/login', () => {
        return HttpResponse.json({
            access_token: 'mock-jwt-token',
            token_type: 'bearer'
        })
    }),

    // Account Mocks (Phase 2 placeholder)
    http.get('/api/accounts', () => {
        return HttpResponse.json({
            data: [
                { id: '1', name: 'ISA Mock', account_type: 'ISA' }
            ]
        })
    }),
]
