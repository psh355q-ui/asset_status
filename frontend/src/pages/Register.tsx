import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Link, useNavigate } from 'react-router-dom';
import { authService } from '../services/auth';
import { useState } from 'react';
import { UserPlus } from 'lucide-react';

const schema = z.object({
    email: z.string().email("유효한 이메일 주소를 입력해주세요."),
    password: z.string().min(6, "비밀번호는 최소 6자 이상이어야 합니다."),
    confirmPassword: z.string()
}).refine((data: { password: string; confirmPassword: string }) => data.password === data.confirmPassword, {
    message: "비밀번호가 일치하지 않습니다.",
    path: ["confirmPassword"],
});

type FormData = z.infer<typeof schema>;

export default function Register() {
    const navigate = useNavigate();
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
        resolver: zodResolver(schema),
    });

    const onSubmit = async (data: FormData) => {
        try {
            setError(null);
            setLoading(true);

            // Call API
            await authService.register({
                email: data.email,
                password: data.password
            });

            // On success, redirect to login
            alert("회원가입이 완료되었습니다. 로그인해주세요.");
            navigate('/login');

        } catch (err: any) {
            console.error(err);
            if (err.response?.status === 400) {
                setError("이미 등록된 이메일입니다.");
            } else {
                setError("회원가입 중 오류가 발생했습니다.");
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="glass-panel" style={{ padding: '2rem' }}>
            <h2 style={{ marginTop: 0, marginBottom: '1.5rem', textAlign: 'center', fontSize: '1.25rem' }}>
                회원가입
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

                <div style={{ marginBottom: '1rem' }}>
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

                <div style={{ marginBottom: '1.5rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                        비밀번호 확인
                    </label>
                    <input
                        {...register('confirmPassword')}
                        className="input"
                        type="password"
                        placeholder="••••••••"
                    />
                    {errors.confirmPassword && (
                        <p style={{ color: 'var(--error)', fontSize: '0.75rem', marginTop: '0.25rem' }}>
                            {errors.confirmPassword.message}
                        </p>
                    )}
                </div>

                <button
                    type="submit"
                    className="btn btn-primary"
                    style={{ width: '100%' }}
                    disabled={loading}
                >
                    {loading ? '가입 중...' : (
                        <>
                            <UserPlus size={18} style={{ marginRight: '0.5rem' }} />
                            회원가입 완료
                        </>
                    )}
                </button>
            </form>

            <div style={{ marginTop: '1.5rem', textAlign: 'center', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                이미 계정이 있으신가요?{' '}
                <Link to="/login" style={{ color: 'var(--primary)', textDecoration: 'none', fontWeight: 500 }}>
                    로그인
                </Link>
            </div>
        </div>
    );
}
