import React from 'react';
import { Cpu } from 'lucide-react';
import Dashboard from './components/Dashboard';

export function App() {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      
      {/* Premium Header/Navigation Bar */}
      <header className="navbar">
        <div className="logo-container">
          <div style={{ 
            background: 'linear-gradient(135deg, var(--accent-cyan), var(--accent-indigo))', 
            padding: '8px', 
            borderRadius: '8px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 4px 10px rgba(6, 182, 212, 0.2)'
          }}>
            <Cpu size={20} color="#0a0f1d" />
          </div>
          <span className="logo-text">PULP & PAPER INTEL</span>
        </div>
        
        <div style={{ display: 'flex', gap: '24px', fontSize: '0.9rem', fontWeight: 500 }}>
          <a href="#dashboard" style={{ color: 'var(--text-primary)', textDecoration: 'none', borderBottom: '2px solid var(--accent-cyan)', paddingBottom: '4px' }}>Dashboard</a>
          <a href="https://github.com/grade-change-intelligence" target="_blank" rel="noreferrer" style={{ color: 'var(--text-secondary)', textDecoration: 'none', transition: 'var(--transition-smooth)' }} onMouseOver={(e) => e.target.style.color = '#f8fafc'} onMouseOut={(e) => e.target.style.color = 'var(--text-secondary)'}>Repository</a>
          <a href="#docs" style={{ color: 'var(--text-secondary)', textDecoration: 'none', transition: 'var(--transition-smooth)' }} onMouseOver={(e) => e.target.style.color = '#f8fafc'} onMouseOut={(e) => e.target.style.color = 'var(--text-secondary)'}>Docs</a>
        </div>
      </header>

      {/* Main Page Layout */}
      <main style={{ flex: 1, backgroundColor: 'var(--bg-primary)' }}>
        <Dashboard />
      </main>

      {/* Footer bar */}
      <footer style={{ 
        textAlign: 'center', 
        padding: '20px 40px', 
        fontSize: '0.8rem', 
        color: 'var(--text-muted)', 
        borderTop: '1px solid var(--border-glass)',
        backgroundColor: 'var(--bg-primary)'
      }}>
        <p>&copy; 2026 Grade Change Intelligence Platform. Developed for pulp & paper manufacturing control.</p>
      </footer>
    </div>
  );
}

export default App;
