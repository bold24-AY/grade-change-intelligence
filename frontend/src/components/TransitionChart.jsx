import React from 'react';
import { 
  ResponsiveContainer, 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend 
} from 'recharts';

export function TransitionChart({ data, dataKey, color = "#06b6d4", title = "Sensor Telemetry" }) {
  // Format dates on X axis
  const formatTime = (isoString) => {
    try {
      const date = new Date(isoString);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    } catch (e) {
      return isoString;
    }
  };

  const gradientId = `colorGradient_${dataKey.replace(/\s+/g, '')}`;

  return (
    <div style={{ width: '100%', height: '300px', marginTop: '16px' }}>
      <h4 style={{ color: '#f8fafc', fontWeight: 600, fontSize: '0.95rem', marginBottom: '12px' }}>{title}</h4>
      <ResponsiveContainer width="100%" height="85%">
        <AreaChart
          data={data}
          margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
        >
          <defs>
            <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={color} stopOpacity={0.4}/>
              <stop offset="95%" stopColor={color} stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#222f54" opacity={0.3} />
          <XAxis 
            dataKey="timestamp" 
            tickFormatter={formatTime} 
            stroke="#64748b" 
            style={{ fontSize: '10px' }}
          />
          <YAxis 
            stroke="#64748b" 
            style={{ fontSize: '10px' }} 
            domain={['auto', 'auto']}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#1b233a', 
              borderColor: '#2d3b5e', 
              borderRadius: '8px',
              color: '#f8fafc',
              fontFamily: 'Inter, sans-serif',
              fontSize: '12px'
            }} 
            labelFormatter={(label) => `Time: ${new Date(label).toLocaleString()}`}
          />
          <Area 
            type="monotone" 
            dataKey={dataKey} 
            stroke={color} 
            strokeWidth={2}
            fillOpacity={1} 
            fill={`url(#${gradientId})`} 
            activeDot={{ r: 6 }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

export default TransitionChart;
