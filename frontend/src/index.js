import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

// Suppress ResizeObserver errors (harmless warnings from animations and dropdowns)
const resizeObserverLoopErrRe = /^[^(ResizeObserver loop limit exceeded|ResizeObserver loop completed with undelivered notifications)]/;
const resizeObserverErrorHandler = (e) => {
  if (
    e.message === 'ResizeObserver loop completed with undelivered notifications.' ||
    e.message === 'ResizeObserver loop limit exceeded'
  ) {
    e.stopImmediatePropagation();
    e.stopPropagation();
  }
};

window.addEventListener('error', resizeObserverErrorHandler);

// Also suppress via console override
const originalError = console.error;
console.error = (...args) => {
  if (
    typeof args[0] === 'string' &&
    (args[0].includes('ResizeObserver') || args[0].includes('resize observer'))
  ) {
    return;
  }
  originalError.apply(console, args);
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
