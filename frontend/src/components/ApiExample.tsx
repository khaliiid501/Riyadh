'use client';

import { useState } from 'react';
import { apiCall, API_BASE_URL } from '@/lib/api';

/**
 * Example component demonstrating API usage
 * This component fetches data from the API and displays it
 */
export default function ApiExample() {
  const [data, setData] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Example API call - adjust endpoint as needed
      const result = await apiCall('/properties');
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 border rounded-lg">
      <h2 className="text-xl font-bold mb-4">API Integration Example</h2>
      
      <div className="mb-4">
        <p className="text-sm text-gray-600">
          <strong>API Base URL:</strong> {API_BASE_URL}
        </p>
      </div>

      <button
        onClick={fetchData}
        disabled={loading}
        className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded disabled:bg-gray-400"
      >
        {loading ? 'Loading...' : 'Fetch Data'}
      </button>

      {error && (
        <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          <strong>Error:</strong> {error}
        </div>
      )}

      {data && (
        <div className="mt-4 p-3 bg-green-100 border border-green-400 rounded">
          <strong>Success!</strong> Data received from API
          <pre className="mt-2 text-sm overflow-auto">
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      )}

      {!data && !loading && !error && (
        <p className="mt-4 text-gray-500">
          Click the button to fetch data from the API
        </p>
      )}
    </div>
  );
}
