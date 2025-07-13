import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export const fetchCases = () =>
  axios.get(`${API_BASE}/cases`).then(res => res.data);

export const sendMessage = (message, caseContext) =>
  axios.post(`${API_BASE}/chat`, { message, case_context: caseContext })
       .then(res => res.data);
