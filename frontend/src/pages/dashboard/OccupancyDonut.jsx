import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

const OccupancyDonut = ({ data = {} }) => {
  const activeTenants = data?.active_tenants || 0;
  const totalCapacity = data?.total_capacity || 1;
  const rate = data?.rate || 0;

  const chartData = [
    { name: 'Occupied', value: activeTenants },
    { name: 'Available', value: Math.max(0, totalCapacity - activeTenants) },
  ];

  const COLORS = ['#3B82F6', 'rgba(255,255,255,0.1)'];

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-black/80 backdrop-blur-md p-2 rounded-lg border border-white/10 text-xs">
          <p className="text-white">{`${payload[0].name}: ${payload[0].value}`}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="glass-card p-6 h-full flex flex-col items-center justify-center relative">
      <h3 className="absolute top-6 left-6 text-sm font-medium uppercase tracking-wider text-white/50">Occupancy</h3>

      <div className="h-48 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              innerRadius={60}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
              stroke="none"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center mt-4">
        <p className="text-3xl font-bold text-white">{rate}%</p>
        <p className="text-xs text-white/40">Full</p>
      </div>

      <div className="mt-[-20px] text-center">
        <p className="text-sm text-blue-300 font-medium">
          {Math.max(0, totalCapacity - activeTenants)} Beds Available
        </p>
      </div>
    </div>
  );
};

export default OccupancyDonut;
