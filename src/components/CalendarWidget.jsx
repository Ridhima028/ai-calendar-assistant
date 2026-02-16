import React, { useState } from 'react';
import { motion } from 'framer-motion';

const CalendarWidget = ({ selectedDate }) => {
  const [currentDate, setCurrentDate] = useState(new Date(2024, 3, 1)); // April 2024

  const getDaysInMonth = (date) => {
    return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
  };

  const getFirstDayOfMonth = (date) => {
    return new Date(date.getFullYear(), date.getMonth(), 1).getDay();
  };

  const daysInMonth = getDaysInMonth(currentDate);
  const firstDay = getFirstDayOfMonth(currentDate);
  const days = [];

  for (let i = 0; i < firstDay; i++) {
    days.push(null);
  }
  for (let i = 1; i <= daysInMonth; i++) {
    days.push(i);
  }

  const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  const dayLabels = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'];

  const goToPreviousMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1));
  };

  const goToNextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1));
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6, delay: 0.2 }}
      className="bg-gradient-to-br from-white to-blue-50 border border-blue-200 rounded-lg p-6 shadow-sm"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-slate-800">
          {months[currentDate.getMonth()]} {currentDate.getFullYear()}
        </h2>
        <div className="flex gap-2">
          <button
            onClick={goToPreviousMonth}
            className="p-1.5 hover:bg-blue-100 rounded-lg transition-colors"
          >
            <span className="text-slate-600">←</span>
          </button>
          <button
            onClick={goToNextMonth}
            className="p-1.5 hover:bg-blue-100 rounded-lg transition-colors"
          >
            <span className="text-slate-600">→</span>
          </button>
        </div>
      </div>

      {/* Day Labels */}
      <div className="grid grid-cols-7 gap-2 mb-4">
        {dayLabels.map((day) => (
          <div
            key={day}
            className="h-8 flex items-center justify-center text-xs font-semibold text-slate-600"
          >
            {day}
          </div>
        ))}
      </div>

      {/* Calendar Days */}
      <div className="grid grid-cols-7 gap-2">
        {days.map((day, index) => (
          <motion.button
            key={index}
            whileHover={day ? { scale: 1.1, backgroundColor: 'rgb(37 99 235 / 0.8)' } : {}}
            className={`h-8 rounded-lg flex items-center justify-center text-sm font-medium transition-all duration-200 ${
              day === 23
                ? 'bg-blue-500 text-white'
                : day
                ? 'text-slate-600 hover:bg-blue-100'
                : 'text-slate-300'
            }`}
          >
            {day}
          </motion.button>
        ))}
      </div>
    </motion.div>
  );
};

export default CalendarWidget;
