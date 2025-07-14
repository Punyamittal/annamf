"use client";

import React, { useState } from "react";
import Link from "next/link";
import { ArrowLeft, Settings, Bell, Shield, Database, RefreshCw } from "lucide-react";

const SettingsPage = () => {
  const [refreshInterval, setRefreshInterval] = useState(5000);
  const [notifications, setNotifications] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);

  const handleSaveSettings = () => {
    alert("Settings saved successfully!");
  };

  const handleReloadModels = () => {
    alert("ML models reloaded successfully!");
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link href="/agrotwin" className="flex items-center space-x-2 text-gray-700 hover:text-green-600 transition-colors">
                <ArrowLeft className="h-5 w-5" />
                <span className="font-medium">Back to AgroTwin</span>
              </Link>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">AgroTwin Settings</span>
            </div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto py-8 px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold mb-8">AgroTwin Settings</h1>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Data Settings */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center space-x-2 mb-6">
                <Database className="h-5 w-5 text-blue-600" />
                <h2 className="text-xl font-semibold">Data Settings</h2>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Auto Refresh Interval
                  </label>
                  <select
                    value={refreshInterval}
                    onChange={(e) => setRefreshInterval(Number(e.target.value))}
                    className="w-full border border-gray-300 rounded-md px-3 py-2"
                  >
                    <option value={2000}>2 seconds</option>
                    <option value={5000}>5 seconds</option>
                    <option value={10000}>10 seconds</option>
                    <option value={30000}>30 seconds</option>
                  </select>
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Auto Refresh</label>
                    <p className="text-xs text-gray-500">Automatically update sensor data</p>
                  </div>
                  <input
                    type="checkbox"
                    checked={autoRefresh}
                    onChange={(e) => setAutoRefresh(e.target.checked)}
                    className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                  />
                </div>
              </div>
            </div>

            {/* Notification Settings */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center space-x-2 mb-6">
                <Bell className="h-5 w-5 text-orange-600" />
                <h2 className="text-xl font-semibold">Notifications</h2>
              </div>

              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Email Notifications</label>
                    <p className="text-xs text-gray-500">Receive alerts via email</p>
                  </div>
                  <input
                    type="checkbox"
                    checked={notifications}
                    onChange={(e) => setNotifications(e.target.checked)}
                    className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">SMS Alerts</label>
                    <p className="text-xs text-gray-500">Receive critical alerts via SMS</p>
                  </div>
                  <input
                    type="checkbox"
                    className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Push Notifications</label>
                    <p className="text-xs text-gray-500">Receive browser notifications</p>
                  </div>
                  <input
                    type="checkbox"
                    className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                  />
                </div>
              </div>
            </div>

            {/* System Settings */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center space-x-2 mb-6">
                <Settings className="h-5 w-5 text-gray-600" />
                <h2 className="text-xl font-semibold">System Settings</h2>
              </div>

              <div className="space-y-4">
                <button
                  onClick={handleReloadModels}
                  className="w-full flex items-center justify-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
                >
                  <RefreshCw className="h-4 w-4" />
                  <span>Reload ML Models</span>
                </button>

                <button className="w-full flex items-center justify-center space-x-2 bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition-colors">
                  <Database className="h-4 w-4" />
                  <span>Clear Cache</span>
                </button>

                <button className="w-full flex items-center justify-center space-x-2 bg-orange-600 text-white px-4 py-2 rounded-md hover:bg-orange-700 transition-colors">
                  <Shield className="h-4 w-4" />
                  <span>Export Data</span>
                </button>
              </div>
            </div>

            {/* Security Settings */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center space-x-2 mb-6">
                <Shield className="h-5 w-5 text-green-600" />
                <h2 className="text-xl font-semibold">Security</h2>
              </div>

              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Two-Factor Authentication</label>
                    <p className="text-xs text-gray-500">Add an extra layer of security</p>
                  </div>
                  <input
                    type="checkbox"
                    className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Session Timeout</label>
                    <p className="text-xs text-gray-500">Auto-logout after inactivity</p>
                  </div>
                  <select className="border border-gray-300 rounded-md px-2 py-1 text-sm">
                    <option>30 minutes</option>
                    <option>1 hour</option>
                    <option>2 hours</option>
                    <option>Never</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* Save Button */}
          <div className="mt-8 flex justify-end">
            <button
              onClick={handleSaveSettings}
              className="bg-green-600 text-white px-6 py-3 rounded-md hover:bg-green-700 transition-colors font-medium"
            >
              Save Settings
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage; 