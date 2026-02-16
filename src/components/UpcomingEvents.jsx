import React from 'react';
import { motion } from 'framer-motion';

const UpcomingEvents = () => {
  const events = [
    {
      id: 1,
      title: 'Project Standup',
      time: 'Tomorrow, 10:00 AM - 10:30 AM',
      icon: '📊',
    },
    {
      id: 2,
      title: 'Weekly Sprint Planning',
      time: 'Apr 26, 3:00 PM - 4:30 PM',
      icon: '🚀',
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6, delay: 0.25 }}
      className="bg-gradient-to-br from-white to-blue-50 border border-blue-200 rounded-lg p-6 shadow-sm"
    >
      <h3 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
        <span>📅</span> Upcoming
      </h3>

      <div className="space-y-3">
        {events.map((event, index) => (
          <motion.div
            key={event.id}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.4, delay: 0.3 + index * 0.1 }}
            className="flex items-start gap-3 p-3 rounded-lg hover:bg-blue-100/50 transition-all duration-200 cursor-pointer"
          >
            <span className="text-xl mt-1">{event.icon}</span>
            <div className="flex-1">
              <p className="text-slate-800 font-medium text-sm">{event.title}</p>
              <p className="text-slate-600 text-xs mt-1">{event.time}</p>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
};

export default UpcomingEvents;
