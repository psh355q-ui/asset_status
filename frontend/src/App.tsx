function App() {
    return (
        <div style={{ padding: '2rem', fontFamily: 'system-ui, sans-serif' }}>
            <h1>🏦 자산관리현황</h1>
            <p>Personal Finance Intelligence System</p>

            <div style={{ marginTop: '2rem', padding: '1rem', background: '#f5f5f5', borderRadius: '8px' }}>
                <h2>✅ 프로젝트 셋업 완료!</h2>
                <ul>
                    <li>백엔드: FastAPI (포트 8000)</li>
                    <li>프론트엔드: React + Vite (포트 5173)</li>
                    <li>데이터베이스: PostgreSQL + PGVector</li>
                    <li>캐시: Redis</li>
                </ul>
            </div>

            <div style={{ marginTop: '1rem', padding: '1rem', background: '#e3f2fd', borderRadius: '8px' }}>
                <strong>다음 단계:</strong>
                <p>/orchestrate 명령으로 M0 (Phase 0) 태스크 시작</p>
            </div>
        </div>
    )
}

export default App
