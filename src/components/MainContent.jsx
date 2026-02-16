import React, { useState } from 'react';
import { motion } from 'framer-motion';
import CalendarWidget from './CalendarWidget';
import ChatInterface from './ChatInterface';
import UpcomingEvents from './UpcomingEvents';

const MainContent = ({ selectedDate, userName }) => {
  const getGreeting = () => {
    const hours = new Date().getHours();
    if (hours < 12) return 'Good morning';
    if (hours < 18) return 'Good afternoon';
    return 'Good evening';
  };

  const formatDate = (date) => {
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    const dayName = days[date.getDay()];
    const monthName = months[date.getMonth()];
    const dayNum = date.getDate();
    return `${dayName}, ${monthName} ${dayNum}`;
  };

  return (
    <div className="flex-1 overflow-auto">
      <div className="p-8 pb-32">
        {/* Header Section */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold text-slate-800 mb-2">
            {getGreeting()}, {userName} 👋
          </h1>
          <p className="text-slate-600 text-lg">{formatDate(selectedDate)}</p>
        </motion.div>

        {/* Stats Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8"
        >
          <StatCard label="meetings today" value="3" icon="📅" />
          <StatCard label="new reminders" value="0" icon="🔔" />
          <StatCard label="future nurtys" value="7" icon="📧" />
        </motion.div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Calendar and Upcoming */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="lg:col-span-1 space-y-6"
          >
            <CalendarWidget selectedDate={selectedDate} />
            <UpcomingEvents />
          </motion.div>

          {/* Chat Interface */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="lg:col-span-2"
          >
            <ChatInterface />
          </motion.div>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ label, value, icon }) => {
  return (
    <motion.div
      whileHover={{ translateY: -4 }}
      className="bg-gradient-to-br from-white to-blue-50 border border-blue-200 rounded-lg p-4 cursor-pointer hover:border-blue-400 transition-all duration-200 shadow-sm"
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-slate-600 text-sm font-medium capitalize">{label}</p>
          <p className="text-2xl font-bold text-slate-800 mt-1">{value}</p>
        </div>
        <span className="text-3xl">{icon}</span>
      </div>
    </motion.div>
  );
};

export default MainContent;
