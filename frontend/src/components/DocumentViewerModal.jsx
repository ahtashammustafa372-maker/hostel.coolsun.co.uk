import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, ZoomIn, ZoomOut, Download } from 'lucide-react';

const DocumentViewerModal = ({ isOpen, onClose, imageUrl, title }) => {
  const [scale, setScale] = useState(1);

  if (!isOpen) return null;

  const handleZoomIn = () => setScale(prev => Math.min(prev + 0.25, 3));
  const handleZoomOut = () => setScale(prev => Math.max(prev - 0.25, 0.5));
  const resetZoom = () => setScale(1);

  const downloadImage = () => {
    const link = document.createElement('a');
    link.href = imageUrl;
    link.download = `${title.replace(/\s+/g, '_')}_${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[1100] flex items-center justify-center p-4 md:p-10">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-[#020617]/90 backdrop-blur-xl"
          />

          {/* Modal Content */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            className="glass-card w-full max-w-6xl h-full max-h-[90vh] flex flex-col overflow-hidden relative z-[1110] border-white/10 shadow-2xl"
          >
            {/* Header */}
            <div className="flex items-center justify-between px-6 py-4 bg-white/5 border-b border-white/10">
              <h3 className="text-sm font-bold text-white tracking-tight">{title}</h3>
              
              <div className="flex items-center gap-3">
                <div className="flex items-center bg-black/40 rounded-xl p-1 border border-white/5">
                  <button
                    onClick={handleZoomOut}
                    className="p-2 text-[#8892b0] hover:text-white hover:bg-white/5 rounded-lg transition-all"
                    title="Zoom Out"
                  >
                    <ZoomOut size={16} />
                  </button>
                  <button
                    onClick={resetZoom}
                    className="px-2 py-1 text-[10px] font-bold text-blue-400 hover:text-blue-300 min-w-[40px]"
                  >
                    {Math.round(scale * 100)}%
                  </button>
                  <button
                    onClick={handleZoomIn}
                    className="p-2 text-[#8892b0] hover:text-white hover:bg-white/5 rounded-lg transition-all"
                    title="Zoom In"
                  >
                    <ZoomIn size={16} />
                  </button>
                </div>

                <button
                  onClick={downloadImage}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-[10px] font-bold rounded-xl transition-all shadow-lg shadow-blue-500/20 uppercase"
                >
                  <Download size={16} />
                  <span className="hidden sm:inline">Download</span>
                </button>

                <button
                  onClick={onClose}
                  className="p-2 text-[#8892b0] hover:text-white hover:bg-white/10 rounded-xl transition-all"
                >
                  <X size={20} />
                </button>
              </div>
            </div>

            {/* Viewer Area */}
            <div className="flex-1 overflow-auto bg-[#0a0f1e] flex items-center justify-center p-4 md:p-8 custom-scrollbar">
              {imageUrl && imageUrl.toLowerCase().endsWith('.pdf') ? (
                <div className="w-full h-full rounded-lg overflow-hidden border border-white/5">
                  <iframe
                    src={`${imageUrl}#toolbar=0&navpanes=0&scrollbar=0`}
                    className="w-full h-full bg-white"
                    title={title}
                  />
                </div>
              ) : (
                <div 
                  style={{ transform: `scale(${scale})`, transition: 'transform 0.2s ease-out' }}
                  className="relative shadow-2xl rounded-lg overflow-hidden flex items-center justify-center"
                >
                  <img 
                    src={imageUrl} 
                    alt={title}
                    className="max-w-full max-h-[70vh] object-contain cursor-zoom-in"
                    onDoubleClick={() => setScale(prev => prev === 1 ? 2 : 1)}
                  />
                </div>
              )}
            </div>

            {/* Footer / Instructions */}
            <div className="px-6 py-3 bg-black/40 border-t border-white/10 flex items-center justify-center gap-6 text-[10px] text-[#8892b0] font-bold tracking-widest uppercase">
               <span>Scroll to Zoom</span>
               <span className="w-1.5 h-1.5 rounded-full bg-blue-500/50"></span>
               <span>Drag to Pan</span>
               <span className="w-1.5 h-1.5 rounded-full bg-blue-500/50"></span>
               <span>Double Click to Toggle 2x</span>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};

export default DocumentViewerModal;
