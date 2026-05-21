import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import App from './App.jsx';
import { CartProvider } from './context/CartContext.jsx';
import Chatbot from './chatbot/Chatbot.jsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <CartProvider>
        <App />
        <Toaster position="top-center" toastOptions={{ className: 'toast-shell' }} />
        <Chatbot />
      </CartProvider>
    </BrowserRouter>
  </React.StrictMode>,
);
