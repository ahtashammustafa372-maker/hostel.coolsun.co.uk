import React from 'react';
import { ArrowUpRight, ArrowDownRight, Clock, TrendingUp } from 'lucide-react';

const RevenueCard = ({ data = {} }) => {
  const collected = data?.current_collected || 0;
  const expenses = data?.current_expenses || 0;
  const netCash = data?.net_cash || (collected - expenses);
  const pending = data?.current_pending || 0;
  const arrears = data?.legacy_arrears || 0;

  return (
    <div className="glass-card p-4 md:p-8 rounded-2xl h-full flex flex-col justify-between relative overflow-hidden group">
      <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity text-green-400">
        <TrendingUp size={80} />
      </div>

      <div>
        <h3 className="text-lg font-bold text-white mb-6 flex items-center">
          Financial Pulse
        </h3>

        <div className="space-y-6">
          <div>
            <p className="text-white/40 text-xs uppercase tracking-wider mb-1 flex items-center">
              <TrendingUp size={14} className="mr-1 text-green-400" /> Net Cash in Hand
            </p>
            <p className="text-3xl font-bold text-green-400">Rs. {netCash.toLocaleString()}</p>
          </div>

          <div className="pt-4 border-t border-white/5 space-y-4">
            <div className="flex justify-between items-center">
              <p className="text-white/40 text-[10px] uppercase tracking-widest font-medium">Total Collected</p>
              <p className="text-sm font-bold text-white">Rs. {collected.toLocaleString()}</p>
            </div>
            
            <div className="flex justify-between items-center text-red-400">
              <p className="text-red-400/60 text-[10px] uppercase tracking-widest font-medium">Total Expenses</p>
              <p className="text-sm font-bold">- Rs. {expenses.toLocaleString()}</p>
            </div>

            <div className="pt-2 flex justify-between items-center opacity-60">
              <p className="text-white/40 text-[10px] uppercase tracking-widest">Pending MTD</p>
              <p className="text-sm font-bold text-yellow-100">Rs. {pending.toLocaleString()}</p>
            </div>

            <div className="flex justify-between items-center opacity-60">
              <p className="text-white/40 text-[10px] uppercase tracking-widest">Arrears</p>
              <p className="text-sm font-bold text-red-100 italic">Rs. {arrears.toLocaleString()}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RevenueCard;
