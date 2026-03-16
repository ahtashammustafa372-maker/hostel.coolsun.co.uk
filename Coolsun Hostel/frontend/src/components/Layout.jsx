import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import AppShell from './AppShell';

const Layout = ({ children }) => {
  const location = useLocation();
  const showSidebar = location.pathname !== '/login';

  return (
    <AppShell showSidebar={showSidebar}>
        {/* Background Mesh */}
        <div className="fixed inset-0 pointer-events-none opacity-20 z-0">
             <div className="absolute top-[-10%] right-[-10%] w-[50%] h-[50%] bg-blue-900/40 blur-[120px] rounded-full" />
             <div className="absolute bottom-[-10%] left-[-10%] w-[50%] h-[50%] bg-purple-900/40 blur-[120px] rounded-full" />
        </div>

        <div className="relative">
            {children}
        </div>
    </AppShell>
  );
};

export default Layout;
