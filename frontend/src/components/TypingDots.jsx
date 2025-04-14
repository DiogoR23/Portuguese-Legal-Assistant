import React from 'react';

const TypingDots = () => {
  return (
    <div className="flex gap-1 items-end">
      <span className="w-2 h-2 bg-gray-400 dark:bg-white rounded-full animate-bounce-dot [animation-delay:0s]" />
      <span className="w-2 h-2 bg-gray-400 dark:bg-white rounded-full animate-bounce-dot [animation-delay:0.2s]" />
      <span className="w-2 h-2 bg-gray-400 dark:bg-white rounded-full animate-bounce-dot [animation-delay:0.4s]" />
    </div>
  );
};

export default TypingDots;
