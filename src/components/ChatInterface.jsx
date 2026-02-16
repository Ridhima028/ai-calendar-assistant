import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'ai',
      content: 'Schedule a team meeting for tomorrow at 3 PM',
      action: true,
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [showDialog, setShowDialog] = useState(false);
  const [dialogInfo, setDialogInfo] = useState({
    title: 'Team Meeting',
    time: 'Tomorrow, 3:00 PM - 4:00 PM',
    attendees: ['John', 'Sarah', 'Amir', 'You'],
    reminder: '30m before',
  });

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (inputValue.trim()) {
      const newMessage = {
        id: Date.now(),
        type: 'user',
        content: inputValue,
      };
      setMessages([...messages, newMessage]);
      setInputValue('');

      // Simulate AI response
      setTimeout(() => {
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now(),
            type: 'ai',
            content: 'Schedule a team meeting for tomorrow at 3 PM',
            action: true,
          },
        ]);
      }, 500);
    }
  };

  const handleConfirmDialog = () => {
    setShowDialog(false);
    setMessages((prev) => [
      ...prev,
      {
        id: Date.now(),
        type: 'system',
        content: `✓ Team Meeting scheduled for ${dialogInfo.time}`,
      },
    ]);
  };

  const handleActionClick = () => {
    setShowDialog(true);
  };

  return (
    <>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.3 }}
        className="bg-gradient-to-br from-white to-blue-50 border border-blue-200 rounded-lg flex flex-col h-[600px] relative shadow-sm"
      >
        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.3 }}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {message.type === 'ai' && (
                  <div className="flex gap-3 max-w-xs">
                  <div className="w-8 h-8 rounded-full bg-blue-100 border border-blue-300 flex items-center justify-center flex-shrink-0 text-blue-600">
                    🤖
                  </div>
                  <div className="flex-1">
                    <div className="bg-blue-100/50 border border-blue-200 rounded-lg px-4 py-3">
                      <p className="text-slate-800 text-sm">{message.content}</p>
                      </div>
                      {message.action && (
                        <motion.button
                          whileHover={{ scale: 1.05 }}
                          onClick={handleActionClick}
                          className="mt-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white text-sm rounded-lg transition-colors"
                        >
                          Confirm
                        </motion.button>
                      )}
                    </div>
                  </div>
                )}

                {message.type === 'user' && (
                  <div className="bg-blue-600 rounded-lg px-4 py-3 max-w-xs">
                    <p className="text-white text-sm">{message.content}</p>
                  </div>
                )}

                {message.type === 'system' && (
                  <div className="w-full">
                    <div className="bg-green-100 border border-green-300 rounded-lg px-4 py-3 text-center">
                      <p className="text-green-700 text-sm">{message.content}</p>
                    </div>
                  </div>
                )}
              </motion.div>
            ))}
          </AnimatePresence>
        </div>

        {/* Input Area */}
        <div className="border-t border-blue-200 p-4">
          <form onSubmit={handleSendMessage} className="flex gap-2">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="How can I help you?"
              className="flex-1 bg-white border border-blue-200 rounded-lg px-4 py-3 text-slate-800 placeholder-slate-400 focus:outline-none focus:border-blue-500 transition-colors"
            />
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              type="submit"
              className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              Send
            </motion.button>
          </form>
        </div>
      </motion.div>

      {/* Confirmation Dialog - Rendered outside to avoid positioning issues */}
      <AnimatePresence>
        {showDialog && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setShowDialog(false)}
              className="fixed inset-0 bg-black/50 z-40"
            />
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-gradient-to-br from-white to-blue-50 border border-blue-300 rounded-lg p-6 max-w-md w-full mx-4 z-50 shadow-xl"
            >
              <div className="flex items-start gap-4 mb-4">
                <div className="w-10 h-10 rounded-lg bg-blue-100 border border-blue-300 flex items-center justify-center text-blue-600 flex-shrink-0">
                  📅
                </div>
                <div>
                  <h2 className="text-slate-800 font-bold text-lg mb-1">{dialogInfo.title}</h2>
                  <p className="text-slate-600 text-sm">{dialogInfo.time}</p>
                </div>
              </div>

              <div className="mb-4 space-y-2">
                <div className="flex items-center gap-2 text-slate-700 text-sm">
                  <span>👥</span>
                  <span>{dialogInfo.attendees.join(', ')}</span>
                </div>
                <div className="flex items-center gap-2 text-slate-700 text-sm">
                  <span>🔔</span>
                  <span>Reminder: {dialogInfo.reminder}</span>
                </div>
              </div>

              <div className="flex gap-3">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setShowDialog(false)}
                  className="flex-1 px-4 py-2 border border-blue-300 text-slate-700 rounded-lg hover:bg-blue-100 transition-colors"
                >
                  Cancel
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleConfirmDialog}
                  className="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors font-medium"
                >
                  Confirm
                </motion.button>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
};

export default ChatInterface;
