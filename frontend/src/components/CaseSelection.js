import React, { useEffect, useState } from 'react';
import { fetchCases } from '../services/api';
import { useNavigate } from 'react-router-dom';

export default function CaseSelection() {
  const [cases, setCases] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchCases().then(data => setCases(data));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Select a Case</h1>
      <ul>
        {cases.map(c => (
          <li key={c.id} className="mb-4 border p-4 rounded">
            <h2 className="text-lg font-semibold">{c.name}</h2>
            <p>{c.specialty} - {c.difficulty}</p>
            <button
              className="bg-blue-500 text-white px-4 py-2 mt-2 rounded"
              onClick={() => navigate(`/chat/${c.id}`, { state: c })}
            >
              Start Case
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
