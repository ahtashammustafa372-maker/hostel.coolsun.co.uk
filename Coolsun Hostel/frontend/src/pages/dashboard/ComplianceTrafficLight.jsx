import React from 'react';
import { motion } from 'framer-motion';
import { AlertCircle } from 'lucide-react';

const ComplianceTrafficLight = ({ data = {} }) => {
  const criticalCount = data?.CRITICAL || 0;
  const warningCount = data?.WARNING || 0;
  const safeCount = (data?.NORMAL || 0) + (data?.VERIFIED || 0);

  return (
    <div className="glass-card p-4 flex flex-col items-center justify-center space-y-6 relative group">
      <div className="flex items-center justify-center space-x-2">
        <h3 className="text-sm font-medium uppercase tracking-wider text-white/50">Compliance Health</h3>
        <div className="relative group/info">
          <AlertCircle size={14} className="text-white/20 hover:text-white transition-colors cursor-help" />
          <div className="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 w-48 p-2 bg-black/90 text-[10px] text-white rounded-lg opacity-0 group-hover/info:opacity-100 transition-opacity pointer-events-none z-50 border border-white/10 shadow-2xl">
            <p className="font-bold mb-1">Aging Protocol:</p>
            <p>• Red: Expired + 7 Days Grace</p>
            <p>• Yellow: Expired (In Grace)</p>
            <p>• Green: Verified & Valid</p>
          </div>
        </div>
      </div>

      <div className="flex justify-around w-full">
        {/* Red Light */}
        <div className="flex flex-col items-center cursor-pointer group">
          <div className="relative">
            <motion.div
              className={`h-14 w-14 md:h-16 md:w-16 rounded-full flex items-center justify-center border-4 transition-all ${criticalCount > 0
                ? 'bg-red-500/20 border-red-500 text-red-500 shadow-[0_0_15px_rgba(239,68,68,0.5)]'
                : 'bg-black/20 border-white/10 text-white/20'
                }`}
            >
              <span className="text-xl font-bold">{criticalCount}</span>
            </motion.div>
          </div>
          <span className="text-[10px] md:text-xs mt-2 text-white/40 group-hover:text-red-400 transition-colors">Critical</span>
        </div>

        {/* Yellow Light */}
        <div className="flex flex-col items-center cursor-pointer group">
          <div className="relative">
            <motion.div
              animate={warningCount > 0 ? { boxShadow: ["0 0 0px #eab308", "0 0 15px #eab308", "0 0 0px #eab308"] } : {}}
              transition={{ duration: 3, repeat: Infinity }}
              className={`h-14 w-14 md:h-16 md:w-16 rounded-full flex items-center justify-center border-4 transition-all ${warningCount > 0
                ? 'bg-yellow-500/20 border-yellow-500 text-yellow-500 shadow-[0_0_10px_rgba(234,179,8,0.3)]'
                : 'bg-black/20 border-white/10 text-white/20'
                }`}
            >
              <span className="text-xl font-bold">{warningCount}</span>
            </motion.div>
          </div>
          <span className="text-[10px] md:text-xs mt-2 text-white/40 group-hover:text-yellow-400 transition-colors">Warning</span>
        </div>

        {/* Green Light */}
        <div className="flex flex-col items-center">
          <div className={`h-14 w-14 md:h-16 md:w-16 rounded-full flex items-center justify-center border-4 border-green-500/50 bg-green-500/10 text-green-500`}>
            <span className="text-xl font-bold">{safeCount}</span>
          </div>
          <span className="text-[10px] md:text-xs mt-2 text-white/40">Safe</span>
        </div>
      </div>

      <p className="text-xs text-white/30 text-center pt-2">
        Tap a light to view tenant list
      </p>
    </div>
  );
};

export default ComplianceTrafficLight;
