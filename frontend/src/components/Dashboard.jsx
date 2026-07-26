import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  Settings as SettingsIcon, 
  TrendingUp, 
  AlertTriangle, 
  Gauge, 
  RefreshCw,
  Sliders,
  Layers
} from 'lucide-react';
import api from '../services/api';
import TransitionChart from './TransitionChart';

export function Dashboard() {
  const [specs, setSpecs] = useState({});
  const [health, setHealth] = useState(null);
  
  // Simulated telemetry state
  const [telemetry, setTelemetry] = useState({
    pulp_flow_m3h: 450.0,
    consistency_pct: 3.40,
    steam_pressure_bar: 4.20,
    machine_speed_mpm: 850.0
  });

  // Predictions history for chart
  const [history, setHistory] = useState([
    { timestamp: new Date(Date.now() - 40000).toISOString(), pulp_flow_m3h: 450, machine_speed_mpm: 850, is_transitioning: false },
    { timestamp: new Date(Date.now() - 30000).toISOString(), pulp_flow_m3h: 449, machine_speed_mpm: 849, is_transitioning: false },
    { timestamp: new Date(Date.now() - 20000).toISOString(), pulp_flow_m3h: 430, machine_speed_mpm: 830, is_transitioning: false },
    { timestamp: new Date(Date.now() - 10000).toISOString(), pulp_flow_m3h: 400, machine_speed_mpm: 780, is_transitioning: true },
  ]);

  const [activePrediction, setActivePrediction] = useState({
    is_transitioning: false,
    confidence_score: 0.95,
    predicted_target_grade: null,
    anomaly_detected: false
  });

  const [isLoading, setIsLoading] = useState(false);

  // Load initial backend specs & health
  useEffect(() => {
    async function loadInitialData() {
      try {
        const specsData = await api.getSpecs();
        setSpecs(specsData);
        
        const healthData = await api.getHealth();
        setHealth(healthData);
      } catch (err) {
        console.error("Failed to load initial data", err);
      }
    }
    loadInitialData();
  }, []);

  // Whenever sliders change, trigger API prediction
  const handleSliderChange = (key, val) => {
    setTelemetry(prev => ({
      ...prev,
      [key]: parseFloat(val)
    }));
  };

  const handleTriggerPrediction = async () => {
    setIsLoading(true);
    const payload = {
      ...telemetry,
      timestamp: new Date().toISOString()
    };
    
    try {
      const res = await api.predict(payload);
      setActivePrediction(res);
      
      // Append to historical timeline array
      setHistory(prev => [
        ...prev.slice(-9), // Keep last 10 points
        {
          timestamp: payload.timestamp,
          pulp_flow_m3h: payload.pulp_flow_m3h,
          machine_speed_mpm: payload.machine_speed_mpm,
          is_transitioning: res.is_transitioning
        }
      ]);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="dashboard-grid">
      
      {/* 1. System Status Header Banner */}
      <div className="glass-panel" style={{ gridColumn: 'span 12', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          <Activity size={32} color="#06b6d4" className="pulse-animation" />
          <div>
            <h2 style={{ fontSize: '1.2rem', fontWeight: 600 }}>Grade Transition Monitor</h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Real-time machine telemetry & AI-driven transition predictions</p>
          </div>
        </div>
        
        <div style={{ display: 'flex', gap: '20px', fontSize: '0.85rem' }}>
          <div style={{ background: 'var(--bg-tertiary)', padding: '8px 16px', borderRadius: 'var(--border-radius-md)' }}>
            <span style={{ color: 'var(--text-muted)' }}>Backend Model: </span>
            <span style={{ color: 'var(--accent-cyan)', fontWeight: 600 }}>{health?.model_version || 'Loading...'}</span>
          </div>
          <div style={{ background: 'var(--bg-tertiary)', padding: '8px 16px', borderRadius: 'var(--border-radius-md)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Status: </span>
            <span style={{ 
              width: '8px', 
              height: '8px', 
              borderRadius: '50%', 
              backgroundColor: health?.status === 'healthy' || health?.status === 'simulated-local' ? 'var(--status-success)' : 'var(--status-warning)' 
            }}></span>
            <span style={{ fontWeight: 600 }}>{health?.status === 'simulated-local' ? 'Mock Mode' : 'Online'}</span>
          </div>
        </div>
      </div>

      {/* 2. Transition Warning Alert (Flashing/Glowing when active) */}
      {activePrediction.is_transitioning && (
        <div className="glass-panel" style={{ 
          gridColumn: 'span 12', 
          background: 'rgba(239, 68, 68, 0.1)', 
          borderColor: 'var(--status-danger)',
          display: 'flex',
          alignItems: 'center',
          gap: '15px',
          boxShadow: '0 0 20px rgba(239, 68, 68, 0.2)'
        }}>
          <AlertTriangle color="var(--status-danger)" size={28} />
          <div>
            <h3 style={{ color: '#ff7b7b', fontSize: '1.05rem', fontWeight: 600 }}>Grade Transition In Progress</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
              Machine state shifting. Target Grade: <strong style={{ color: 'var(--text-primary)' }}>{activePrediction.predicted_target_grade || 'Determining...'}</strong> | Confidence: {Math.round(activePrediction.confidence_score * 100)}%
            </p>
          </div>
        </div>
      )}

      {/* 3. Slider Simulation Panel */}
      <div className="glass-panel" style={{ gridColumn: 'span 4' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
          <Sliders size={20} color="var(--accent-indigo)" />
          <h3 style={{ fontSize: '1rem', fontWeight: 600 }}>DCS Controller Simulator</h3>
        </div>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '6px' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Thick Stock Flow</span>
              <strong style={{ color: 'var(--accent-cyan)' }}>{telemetry.pulp_flow_m3h} m³/h</strong>
            </div>
            <input 
              type="range" 
              min="200" 
              max="1000" 
              value={telemetry.pulp_flow_m3h} 
              onChange={(e) => handleSliderChange('pulp_flow_m3h', e.target.value)}
              style={{ width: '100%' }}
            />
          </div>

          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '6px' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Fiber Consistency</span>
              <strong style={{ color: 'var(--accent-cyan)' }}>{telemetry.consistency_pct} %</strong>
            </div>
            <input 
              type="range" 
              min="1.0" 
              max="5.0" 
              step="0.05"
              value={telemetry.consistency_pct} 
              onChange={(e) => handleSliderChange('consistency_pct', e.target.value)}
              style={{ width: '100%' }}
            />
          </div>

          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '6px' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Machine Speed</span>
              <strong style={{ color: 'var(--accent-cyan)' }}>{telemetry.machine_speed_mpm} mpm</strong>
            </div>
            <input 
              type="range" 
              min="500" 
              max="1500" 
              value={telemetry.machine_speed_mpm} 
              onChange={(e) => handleSliderChange('machine_speed_mpm', e.target.value)}
              style={{ width: '100%' }}
            />
          </div>

          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '6px' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Steam Pressure</span>
              <strong style={{ color: 'var(--accent-cyan)' }}>{telemetry.steam_pressure_bar} bar</strong>
            </div>
            <input 
              type="range" 
              min="1.0" 
              max="6.0" 
              step="0.1"
              value={telemetry.steam_pressure_bar} 
              onChange={(e) => handleSliderChange('steam_pressure_bar', e.target.value)}
              style={{ width: '100%' }}
            />
          </div>

          <button 
            className="btn-primary" 
            onClick={handleTriggerPrediction} 
            disabled={isLoading}
            style={{ width: '100%', marginTop: '10px', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '8px' }}
          >
            {isLoading ? <RefreshCw className="spin-animation" size={16} /> : <Gauge size={16} />}
            Evaluate Machine State
          </button>
        </div>
      </div>

      {/* 4. Live Charts Area */}
      <div className="glass-panel" style={{ gridColumn: 'span 8', display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <TrendingUp size={20} color="var(--accent-cyan)" />
            <h3 style={{ fontSize: '1rem', fontWeight: 600 }}>Live Telemetry Streams</h3>
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Updated live on state evaluation</span>
        </div>
        
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <TransitionChart 
            data={history} 
            dataKey="pulp_flow_m3h" 
            title="Thick Stock Pulp Flow (m³/h)" 
            color="var(--accent-cyan)" 
          />
          <TransitionChart 
            data={history} 
            dataKey="machine_speed_mpm" 
            title="Machine Speed (mpm)" 
            color="var(--accent-indigo)" 
          />
        </div>
      </div>

      {/* 5. Grade Specifications Catalog */}
      <div className="glass-panel" style={{ gridColumn: 'span 12' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
          <Layers size={20} color="var(--accent-cyan)" />
          <h3 style={{ fontSize: '1rem', fontWeight: 600 }}>Target Grade Tolerances</h3>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
          {Object.entries(specs).map(([key, spec]) => (
            <div key={key} style={{ background: 'var(--bg-secondary)', padding: '16px', borderRadius: 'var(--border-radius-md)', border: '1px solid var(--border-glass)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px', alignItems: 'center' }}>
                <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--accent-cyan)' }}>{key}</span>
                <span style={{ fontSize: '0.75rem', background: 'rgba(99, 102, 241, 0.1)', color: 'var(--accent-indigo)', padding: '2px 8px', borderRadius: '4px', fontWeight: 600 }}>
                  {spec.nominal_machine_speed_mpm} mpm
                </span>
              </div>
              <h4 style={{ fontSize: '0.9rem', color: 'var(--text-primary)', marginBottom: '12px' }}>{spec.name}</h4>
              
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '6px' }}>
                <span>Basis Weight:</span>
                <span style={{ color: 'var(--text-primary)' }}>{spec.target_basis_weight_gsm} ± {spec.tolerance_basis_weight_gsm} gsm</span>
              </div>
              
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                <span>Moisture Target:</span>
                <span style={{ color: 'var(--text-primary)' }}>{spec.target_moisture_pct} ± {spec.tolerance_moisture_pct} %</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
