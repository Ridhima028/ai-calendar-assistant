import React, { useState } from 'react';
import { motion } from 'framer-motion';

const Sidebar = () => {
  const [activeItem, setActiveItem] = useState('calendar');

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'calendar', label: 'Calendar', icon: '📅' },
    { id: 'assistant', label: 'AI Assistant', icon: '🤖' },
    { id: 'settings', label: 'Settings', icon: '⚙️' },
  ];

  return (
    <div className="w-64 bg-gradient-to-b from-blue-100 to-cyan-50 border-r border-blue-200 flex flex-col p-6 h-screen overflow-y-auto">
      {/* Logo */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex items-center gap-3 mb-12"
      >
        <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-cyan-300 rounded-lg flex items-center justify-center">
          <span className="text-white font-bold text-lg">🗓️</span>
        </div>
        <h1 className="text-xl font-bold text-slate-700">Calendar AI</h1>
      </motion.div>

      {/* Navigation */}
      <nav className="flex-1 space-y-2">
        {menuItems.map((item, index) => (
          <motion.button
            key={item.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            onClick={() => setActiveItem(item.id)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
              activeItem === item.id
                ? 'bg-blue-500 text-white'
                : 'text-slate-600 hover:bg-blue-100'
            }`}
          >
            <span className="text-xl">{item.icon}</span>
            <span className="font-medium">{item.label}</span>
          </motion.button>
        ))}
      </nav>

      {/* User Profile */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.5 }}
        className="pt-6 border-t border-blue-200"
      >
        <div className="flex items-center gap-3 p-3 rounded-lg bg-blue-200/30">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-cyan-300 rounded-full flex items-center justify-center text-white font-bold">
            R
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium text-slate-700">Riya</p>
            <p className="text-xs text-slate-500">Premium User</p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Sidebar;
