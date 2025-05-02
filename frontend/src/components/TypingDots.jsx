/*
TypingDots.jsx

A simple component that shows three dots bouncing in a row to indicate typing.
This component is used to indicate that the bot is typing a response. It uses Tailwind CSS for styling and animation.
The component consists of three dots that bounce in a row. The dots are styled with a gray background color and rounded corner. The animation is achieved using the `animate-bounce-dot` class, which is defined in the Tailwind CSS configuration file.
The `animation-delay` property is used to create a staggered effect, where each dot bounces at a different time. The first dot has no delay, the second dot has a delay of 0.2 seconds, and the third dot has a delay of 0.4 seconds.
This component is used in the chat interface to indicate that the bot is typing a response. It is a simple and effective way to show the user that the bot is processing their request and will respond shortly.
*/

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
