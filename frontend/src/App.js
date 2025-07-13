import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CaseSelection from './components/CaseSelection';
import ChatScreen from './components/ChatScreen';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<CaseSelection />} />
        <Route path="/chat/:id" element={<ChatScreen />} />
      </Routes>
    </Router>
  );
}

export default App;
