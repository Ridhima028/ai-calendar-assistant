import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Sidebar from './Sidebar';
import MainContent from './MainContent';

const Dashboard = () => {
  const [selectedDate, setSelectedDate] = useState(new Date(2024, 3, 23)); // April 23, 2024
  const [userName, setUserName] = useState('Riya');

  return (
    <div className="flex h-screen bg-gradient-to-br from-blue-50 via-cyan-50 to-blue-100 text-slate-800 overflow-hidden relative">
      {/* Animated Gradient Background Elements */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        {/* Top Right Gradient Orb */}
        <motion.div
          animate={{
            y: [0, 30, 0],
            x: [0, 20, 0],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
          className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-blue-300 to-cyan-200 rounded-full filter blur-3xl opacity-20"
        />

        {/* Bottom Left Gradient Orb */}
        <motion.div
          animate={{
            y: [0, -30, 0],
            x: [0, -20, 0],
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
          className="absolute -bottom-40 -left-40 w-96 h-96 bg-gradient-to-tr from-cyan-300 to-blue-200 rounded-full filter blur-3xl opacity-15"
        />

        {/* Top Left Accent */}
        <motion.div
          animate={{
            rotate: [0, 360],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: 'linear',
          }}
          className="absolute top-10 left-1/4 w-64 h-64 bg-gradient-to-br from-blue-200 to-transparent rounded-full filter blur-2xl opacity-10"
        />

        {/* Center Gradient */}
        <motion.div
          animate={{
            scale: [1, 1.1, 1],
          }}
          transition={{
            duration: 6,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
          className="absolute top-1/3 right-1/4 w-72 h-72 bg-gradient-to-b from-cyan-200 to-blue-100 rounded-full filter blur-3xl opacity-10"
        />

        {/* Bottom Right Accent */}
        <motion.div
          animate={{
            y: [0, -40, 0],
          }}
          transition={{
            duration: 7,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
          className="absolute bottom-20 right-10 w-48 h-48 bg-gradient-to-tl from-blue-300 to-cyan-100 rounded-full filter blur-2xl opacity-10"
        />

        {/* Diagonal Wave Lines */}
        <svg
          className="absolute inset-0 w-full h-full opacity-5"
          preserveAspectRatio="none"
          viewBox="0 0 1200 800"
        >
          <defs>
            <linearGradient id="waveGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#3b82f6" />
              <stop offset="100%" stopColor="#06b6d4" />
            </linearGradient>
          </defs>
          <path
            d="M 0 100 Q 300 50, 600 100 T 1200 100"
            fill="none"
            stroke="url(#waveGradient)"
            strokeWidth="2"
          />
          <path
            d="M 0 300 Q 300 250, 600 300 T 1200 300"
            fill="none"
            stroke="url(#waveGradient)"
            strokeWidth="2"
          />
          <path
            d="M 0 500 Q 300 450, 600 500 T 1200 500"
            fill="none"
            stroke="url(#waveGradient)"
            strokeWidth="2"
          />
          <path
            d="M 0 700 Q 300 650, 600 700 T 1200 700"
            fill="none"
            stroke="url(#waveGradient)"
            strokeWidth="2"
          />
        </svg>

        {/* Dotted Grid Pattern */}
        <div className="absolute inset-0 opacity-5">
          <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                <circle cx="20" cy="20" r="1" fill="#3b82f6" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" />
          </svg>
        </div>
      </div>

      {/* Main Content */}
      <Sidebar />
      <MainContent selectedDate={selectedDate} userName={userName} />
    </div>
  );
};

export default Dashboard;
