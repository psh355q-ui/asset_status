import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Link, useNavigate } from 'react-router-dom';
import { authService } from '../services/auth';
import { useAuthStore } from '../store/useAuthStore';
import { useState } from 'react';
import { LogIn } from 'lucide-react';

const schema = z.object({
    email: z.string().email("유효한 이메일 주소를 입력해주세요."),
    password: z.string().min(1, "비밀번호를 입력해주세요."),
});

type FormData = z.infer<typeof schema>;

export default function Login() {
    const navigate = useNavigate();
    const login = useAuthStore((state) => state.login);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
        resolver: zodResolver(schema),
    });

    const onSubmit = async (data: FormData) => {
        try {
            setError(null);
            setLoading(true);
            const tokenData = await authService.login(data);

            // Store token (and dummy user info since /me is not ready)
            login(tokenData.access_token, { id: 'user', email: data.email });

            navigate('/dashboard'); // Redirect to dashboard
        } catch (err: any) {
            console.error(err);
            if (err.response?.status === 401) {
                setError("이메일 또는 비밀번호가 일치하지 않습니다.");
            } else {
                setError("로그인 중 오류가 발생했습니다. 다시 시도해주세요.");
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="glass-panel" style={{ padding: '2rem' }}>
            <h2 style={{ marginTop: 0, marginBottom: '1.5rem', textAlign: 'center', fontSize: '1.25rem' }}>
                로그인
            </h2>

            <form onSubmit={handleSubmit(onSubmit)}>
                {error && (
                    <div style={{
                        background: 'rgba(239, 68, 68, 0.2)',
                        color: '#fca5a5',
                        padding: '0.75rem',
                        borderRadius: '0.5rem',
                        marginBottom: '1rem',
                        fontSize: '0.875rem'
                    }}>
                        {error}
                    </div>
                )}

                <div style={{ marginBottom: '1rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                        이메일
                    </label>
                    <input
                        {...register('email')}
                        className="input"
                        type="email"
                        placeholder="name@example.com"
                    />
                    {errors.email && (
                        <p style={{ color: 'var(--error)', fontSize: '0.75rem', marginTop: '0.25rem' }}>
                            {errors.email.message}
                        </p>
                    )}
                </div>

                <div style={{ marginBottom: '1.5rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                        비밀번호
                    </label>
                    <input
                        {...register('password')}
                        className="input"
                        type="password"
                        placeholder="••••••••"
                    />
                    {errors.password && (
                        <p style={{ color: 'var(--error)', fontSize: '0.75rem', marginTop: '0.25rem' }}>
                            {errors.password.message}
                        </p>
                    )}
                </div>

                <button
                    type="submit"
                    className="btn btn-primary"
                    style={{ width: '100%' }}
                    disabled={loading}
                >
                    {loading ? '로그인 중...' : (
                        <>
                            <LogIn size={18} style={{ marginRight: '0.5rem' }} />
                            로그인
                        </>
                    )}
                </button>
            </form>

            <div style={{ marginTop: '1.5rem', textAlign: 'center', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                계정이 없으신가요?{' '}
                <Link to="/register" style={{ color: 'var(--primary)', textDecoration: 'none', fontWeight: 500 }}>
                    회원가입
                </Link>
            </div>
        </div>
    );
}
