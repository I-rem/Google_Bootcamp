import React, { useState } from 'react';
import { sendMessage } from '../services/api';
import { useLocation } from 'react-router-dom';

export default function ChatScreen() {
  const { state } = useLocation();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    const userMessage = { sender: 'student', text: input };
    setMessages([...messages, userMessage]);

    sendMessage(input, state.name)
      .then(res => {
        setMessages(prev => [...prev, { sender: 'patient', text: res.reply }]);
        setInput('');
      });
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">{state.name}</h1>
      <div className="border p-4 rounded mb-4 h-96 overflow-y-scroll">
        {messages.map((m, i) => (
          <div key={i} className={`${m.sender === 'student' ? 'text-right' : 'text-left'} mb-2`}>
            <span className="inline-block bg-gray-200 px-4 py-2 rounded">{m.text}</span>
          </div>
        ))}
      </div>
      <div className="flex">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          className="border p-2 flex-1 rounded-l"
          placeholder="Ask the patient..."
        />
        <button onClick={handleSend} className="bg-blue-500 text-white px-4 py-2 rounded-r">Send</button>
      </div>
    </div>
  );
}
