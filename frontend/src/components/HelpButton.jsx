import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { HelpCircle, X, Languages } from 'lucide-react';
import { helpContent } from '../data/helpContent';

export const HelpButton = ({ section }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [lang, setLang] = useState('en');

  const content = helpContent[section]?.[lang] || helpContent['dashboard'][lang];

  // Safety Check: If open but no content, close immediately
  if (isOpen && !content) {
    setIsOpen(false);
  }

  // Lock Body Scroll & Esc Key
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === 'Escape') setIsOpen(false);
    };

    if (isOpen) {
      document.body.style.overflow = 'hidden';
      window.addEventListener('keydown', handleEsc);
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
      window.removeEventListener('keydown', handleEsc);
    };
  }, [isOpen]);

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="inset-0 absolute flex items-center justify-center rounded-lg bg-white/5 hover:bg-white/10 text-white/40 hover:text-white transition-all z-20"
        title="Help Guide"
      >
        <HelpCircle size={18} />
      </button>

      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
              className="fixed inset-0 bg-black/60 backdrop-blur-md z-[110] pointer-events-auto"
            />

            {/* Slide-in Panel */}
            <motion.div
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="fixed top-0 right-0 h-full w-80 bg-[#0f172a] border-l border-white/10 shadow-2xl z-[111] p-6 flex flex-col pointer-events-auto"
            >
              <div className="flex justify-between items-center mb-8">
                <h3 className="text-xl font-bold text-white flex items-center">
                  <HelpCircle className="mr-2 text-blue-400" /> Guide
                </h3>
                <button onClick={() => setIsOpen(false)} className="text-white/50 hover:text-white">
                  <X size={24} />
                </button>
              </div>

              {/* Language Toggle */}
              <div className="flex bg-white/5 rounded-lg p-1 mb-6">
                <button
                  onClick={() => setLang('en')}
                  className={`flex-1 py-2 rounded-md text-sm font-medium transition-all ${lang === 'en' ? 'bg-blue-600 text-white' : 'text-white/50 hover:text-white'}`}
                >
                  English
                </button>
                <button
                  onClick={() => setLang('ur')}
                  className={`flex-1 py-2 rounded-md text-sm font-medium transition-all ${lang === 'ur' ? 'bg-green-600 text-white' : 'text-white/50 hover:text-white'}`}
                >
                  Urdu
                </button>
              </div>

              {/* Content */}
              <div className="flex-1 overflow-y-auto scrollbar-hide">
                <h4 className="text-lg font-semibold text-blue-300 mb-4">{content.title}</h4>
                <ul className="space-y-4">
                  {content.steps.map((step, idx) => (
                    <li key={idx} className="flex items-start text-white/80 text-sm leading-relaxed">
                      <span className="bg-white/10 text-white/60 h-5 w-5 rounded-full flex items-center justify-center text-xs mr-3 mt-0.5 flex-shrink-0">
                        {idx + 1}
                      </span>
                      {step}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="mt-auto pt-6 border-t border-white/10 text-center">
                <p className="text-xs text-white/30">Coolsun ERP v1.0 &bull; 2026</p>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
};
