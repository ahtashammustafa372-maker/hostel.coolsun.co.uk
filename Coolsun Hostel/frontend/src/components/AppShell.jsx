import React from 'react';
import Sidebar from './Sidebar';

const AppShell = ({ children, showSidebar }) => {
  return (
    <div className={`fixed inset-0 bg-void overflow-hidden flex ${showSidebar ? 'md:flex-row flex-col' : 'flex-col'}`}>

      {/* Sidebar Area - Hidden on Mobile, Fixed Width on Desktop */}
      {showSidebar && (
        <div className="hidden md:flex w-[260px] flex-shrink-0 h-full relative z-[40]">
          <Sidebar mode="desktop" />
        </div>
      )}

      {/* Main Content Area - Takes remaining space and scrolls internally */}
      <main className="flex-1 flex flex-col h-full overflow-y-auto relative scroll-smooth min-w-0">
        <div className="max-w-[1600px] w-full mx-auto p-4 lg:p-8 pb-32">
          {children}
        </div>
      </main>

      {/* Mobile Bottom Navigation - Visible only on Small Mobile */}
      {showSidebar && (
        <div className="md:hidden flex-shrink-0 relative z-[40]">
          <Sidebar mode="mobile" />
        </div>
      )}

    </div>
  );
};

export default AppShell;
