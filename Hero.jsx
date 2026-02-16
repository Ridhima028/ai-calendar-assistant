import React, { useState } from 'react';
import { motion } from 'framer-motion';

const Hero = () => {
  const [isHoveredPrimary, setIsHoveredPrimary] = useState(false);
  const [isHoveredSecondary, setIsHoveredSecondary] = useState(false);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
        delayChildren: 0.3,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.8, ease: 'easeOut' },
    },
  };

  const floatingVariants = {
    initial: { y: 0 },
    animate: {
      y: [0, -20, 0],
      transition: {
        duration: 6,
        repeat: Infinity,
        ease: 'easeInOut',
      },
    },
  };

  const orbVariants = {
    animate: {
      boxShadow: [
        '0 0 20px rgba(59, 130, 246, 0.5)',
        '0 0 40px rgba(59, 130, 246, 0.8)',
        '0 0 20px rgba(59, 130, 246, 0.5)',
      ],
      transition: {
        duration: 3,
        repeat: Infinity,
        ease: 'easeInOut',
      },
    },
  };

  const cards = [
    { title: 'Task Lists', icon: '✓', position: 'top-12 left-1/2 -translate-x-1/2 -translate-y-24' },
    { title: 'Workflows', icon: '⚡', position: 'bottom-12 right-1/2 translate-x-1/2 translate-y-24' },
    { title: 'Analytics', icon: '📊', position: 'top-1/2 -translate-y-1/2 left-0 -translate-x-24' },
    { title: 'Insights', icon: '💡', position: 'top-1/2 -translate-y-1/2 right-0 translate-x-24' },
  ];

  return (
    <div className="relative min-h-screen w-full overflow-hidden">
      {/* Gradient Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-950 via-blue-950 to-black" />

      {/* Radial Glow Effect */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-blue-500 rounded-full filter blur-3xl opacity-20 animate-pulse" />

      {/* Content */}
      <div className="relative z-10 h-screen flex flex-col items-center justify-center px-4 md:px-8">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="flex flex-col items-center justify-center max-w-4xl"
        >
          {/* Center Orb */}
          <motion.div
            variants={orbVariants}
            animate="animate"
            className="mb-12 md:mb-16"
          >
            <div className="w-32 h-32 md:w-40 md:h-40 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 shadow-2xl relative">
              <div className="absolute inset-0 rounded-full bg-blue-300 opacity-20 blur-xl animate-pulse" />
              <div className="absolute inset-2 rounded-full border border-blue-300 opacity-30" />
            </div>
          </motion.div>

          {/* Headline */}
          <motion.h1
            variants={itemVariants}
            className="text-4xl md:text-6xl lg:text-7xl font-bold text-center text-white mb-6 md:mb-8 leading-tight"
          >
            Your AI assistant for <br />
            <span className="bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent">
              smarter productivity
            </span>
          </motion.h1>

          {/* Subtext */}
          <motion.p
            variants={itemVariants}
            className="text-lg md:text-xl text-gray-400 text-center mb-10 md:mb-12 max-w-2xl leading-relaxed"
          >
            Harness the power of AI automation to streamline your workflow, boost efficiency, and unlock new levels of productivity with intelligent task management and real-time insights.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            variants={itemVariants}
            className="flex flex-col md:flex-row gap-4 md:gap-6 w-full md:w-auto justify-center"
          >
            {/* Primary Button */}
            <motion.button
              onHoverStart={() => setIsHoveredPrimary(true)}
              onHoverEnd={() => setIsHoveredPrimary(false)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="relative px-8 md:px-10 py-3 md:py-4 font-semibold text-base md:text-lg text-white rounded-lg overflow-hidden group transition-all duration-300"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-blue-600 transition-all duration-300"
                style={{
                  boxShadow: isHoveredPrimary
                    ? '0 0 30px rgba(59, 130, 246, 0.8)'
                    : '0 0 15px rgba(59, 130, 246, 0.5)',
                }} />
              <span className="relative z-10">Get Started</span>
            </motion.button>

            {/* Secondary Button */}
            <motion.button
              onHoverStart={() => setIsHoveredSecondary(true)}
              onHoverEnd={() => setIsHoveredSecondary(false)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="relative px-8 md:px-10 py-3 md:py-4 font-semibold text-base md:text-lg text-blue-300 rounded-lg overflow-hidden backdrop-blur-md border border-blue-400 border-opacity-30 hover:border-opacity-60 transition-all duration-300 bg-blue-500 bg-opacity-10 hover:bg-opacity-20"
              style={{
                boxShadow: isHoveredSecondary
                  ? '0 0 20px rgba(147, 197, 253, 0.4)'
                  : 'none',
              }}
            >
              <span className="relative z-10">See It in Action</span>
            </motion.button>
          </motion.div>
        </motion.div>

        {/* Floating Cards */}
        <div className="absolute inset-0 pointer-events-none">
          {cards.map((card, index) => (
            <motion.div
              key={index}
              variants={floatingVariants}
              initial="initial"
              animate="animate"
              style={{ animationDelay: `${index * 0.5}s` }}
              className={`absolute w-32 md:w-40 h-32 md:h-40 ${card.position}`}
            >
              {/* Connection Line */}
              <svg className="absolute inset-0 w-full h-full" style={{ pointerEvents: 'none' }}>
                <line
                  x1="50%"
                  y1="50%"
                  x2="50%"
                  y2="50%"
                  stroke="rgba(59, 130, 246, 0.3)"
                  strokeWidth="2"
                  strokeDasharray="5,5"
                />
              </svg>

              {/* Card */}
              <div className="absolute inset-0 rounded-2xl backdrop-blur-md bg-white bg-opacity-5 border border-blue-400 border-opacity-20 shadow-xl p-4 md:p-6 flex flex-col items-center justify-center hover:border-opacity-40 hover:bg-opacity-10 transition-all duration-300 hover:shadow-2xl hover:shadow-blue-500/50">
                <div className="text-3xl md:text-4xl mb-2 md:mb-3">{card.icon}</div>
                <h3 className="text-white font-semibold text-center text-sm md:text-base">
                  {card.title}
                </h3>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Bottom Gradient Fade */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-slate-950 to-transparent pointer-events-none" />
    </div>
  );
};

export default Hero;
