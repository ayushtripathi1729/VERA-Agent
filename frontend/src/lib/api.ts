import axios from 'axios';

/**
 * V.E.R.A. API Gateway Configuration
 * This bridge connects the Next.js HUD to the Render Python Node.
 */

// We pull the URL from Vercel's Environment Variables. 
// If it's missing, it defaults to localhost for your local development.
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: BACKEND_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  // Set a 30-second timeout for complex AI reasoning tasks
  timeout: 30000, 
});

/**
 * RESPONSE INTERCEPTOR
 * Intercepts incoming neural data to ensure it matches our LogEntry format.
 */
api.interceptors.response.use(
  (response) => {
    // If the backend returns a successful task execution
    return response;
  },
  (error) => {
    // Handle "Connection Refused" or "Server Down" errors
    const errorMessage = error.response?.data?.detail || "NEURAL_LINK_TIMEOUT: Backend Unreachable.";
    
    // We modify the error so the Frontend Terminal can catch it and display it
    return Promise.reject({
      message: errorMessage,
      status: 'ERROR',
      timestamp: new Date().toLocaleTimeString(),
    });
  }
);

/**
 * API ENDPOINTS
 * Clean wrappers for our backend calls
 */
export const veraService = {
  // Main execution endpoint for instructions
  runInstruction: async (instruction: string) => {
    return await api.post('/run', { instruction });
  },

  // Health check to verify the link status in the HudHeader
  checkHealth: async () => {
    return await api.get('/health');
  }
};
