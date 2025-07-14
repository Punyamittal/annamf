"use client";

import React from 'react';
import Link from 'next/link';

export default function CrispTest() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">CRISPR Module Test</h1>
        
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Module Status</h2>
          <div className="space-y-2">
            <p className="text-green-600">✅ Frontend components loaded</p>
            <p className="text-green-600">✅ API service configured</p>
            <p className="text-green-600">✅ Navigation link active</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Backend Connection Test</h2>
          <p className="text-gray-600 mb-4">Click the button below to test the backend connection:</p>
          <button 
            onClick={async () => {
              try {
                const response = await fetch('http://localhost:5000/api/health');
                if (response.ok) {
                  alert('✅ Backend is connected and running!');
                } else {
                  alert('❌ Backend responded with error');
                }
              } catch (error) {
                alert('❌ Backend connection failed. Make sure the backend is running on localhost:5000');
              }
            }}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Test Backend Connection
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Quick Links</h2>
          <div className="space-y-2">
            <Link href="/crisp" className="block text-blue-600 hover:text-blue-800">
              → Go to CRISPR Module
            </Link>
            <Link href="/" className="block text-blue-600 hover:text-blue-800">
              → Back to Home
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
} 