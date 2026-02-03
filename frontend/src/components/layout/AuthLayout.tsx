import { Outlet, Link } from 'react-router-dom';
import { TrendingUp } from 'lucide-react';
import './AuthLayout.css';

export default function AuthLayout() {
    return (
        <div className="auth-container">
            {/* Background Effects */}
            <div className="gradient-blob blob-1" />
            <div className="gradient-blob blob-2" />

            <div className="auth-content">
                {/* Brand Header */}
                <div className="brand-area">
                    <Link to="/" style={{ textDecoration: 'none', display: 'inline-block' }}>
                        <TrendingUp className="brand-icon" />
                        <h1 className="brand-title">AI Asset Status</h1>
                    </Link>
                </div>

                {/* Child Pages (Login/Register) */}
                <Outlet />
            </div>
        </div>
    );
}
