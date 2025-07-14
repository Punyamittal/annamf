"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { Home, BarChart3, Settings, Thermometer, Droplets, Sun, Wind } from "lucide-react";

// Mock data for demonstration
const mockFarms = [
  {
    id: "1",
    name: "Green Valley Farm",
    state: "Punjab",
    district: "Amritsar",
    plots: 5,
    sensors: 12
  },
  {
    id: "2", 
    name: "Organic Paradise",
    state: "Karnataka",
    district: "Mysore",
    plots: 3,
    sensors: 8
  },
  {
    id: "3",
    name: "Tech Farm Solutions",
    state: "Maharashtra", 
    district: "Nashik",
    plots: 7,
    sensors: 18
  }
];

const mockSensorReadings = [
  {
    id: "1",
    sensor: { name: "Temperature Sensor" },
    plot: { farm: { name: "Green Valley Farm", state: "Punjab" }, crop: { name: "Wheat" } },
    value: 28.5,
    unit: "°C",
    timestamp: new Date()
  },
  {
    id: "2",
    sensor: { name: "Humidity Sensor" },
    plot: { farm: { name: "Green Valley Farm", state: "Punjab" }, crop: { name: "Wheat" } },
    value: 65,
    unit: "%",
    timestamp: new Date()
  },
  {
    id: "3",
    sensor: { name: "Soil Moisture" },
    plot: { farm: { name: "Green Valley Farm", state: "Punjab" }, crop: { name: "Wheat" } },
    value: 42,
    unit: "%",
    timestamp: new Date()
  },
  {
    id: "4",
    sensor: { name: "Light Sensor" },
    plot: { farm: { name: "Organic Paradise", state: "Karnataka" }, crop: { name: "Rice" } },
    value: 850,
    unit: "lux",
    timestamp: new Date()
  },
  {
    id: "5",
    sensor: { name: "Wind Speed" },
    plot: { farm: { name: "Tech Farm Solutions", state: "Maharashtra" }, crop: { name: "Cotton" } },
    value: 12,
    unit: "km/h",
    timestamp: new Date()
  },
  {
    id: "6",
    sensor: { name: "pH Sensor" },
    plot: { farm: { name: "Tech Farm Solutions", state: "Maharashtra" }, crop: { name: "Cotton" } },
    value: 6.8,
    unit: "pH",
    timestamp: new Date()
  }
];

const DashboardPage = () => {
  const [refreshInterval, setRefreshInterval] = useState(5000);
  const [selectedFarmId, setSelectedFarmId] = useState<string>("1");
  const [liveReadings, setLiveReadings] = useState(mockSensorReadings);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  // Simulate live data updates
  useEffect(() => {
    const interval = setInterval(() => {
      setLiveReadings(prev => prev.map(reading => ({
        ...reading,
        value: reading.value + (Math.random() - 0.5) * 2,
        timestamp: new Date()
      })));
      setLastUpdate(new Date());
    }, refreshInterval);
    return () => clearInterval(interval);
  }, [refreshInterval]);

  const handleReloadModels = () => {
    alert("ML models reloaded successfully!");
  };

  const getSensorIcon = (sensorName: string) => {
    if (sensorName.includes("Temperature")) return <Thermometer className="h-4 w-4 text-red-500" />;
    if (sensorName.includes("Humidity") || sensorName.includes("Moisture")) return <Droplets className="h-4 w-4 text-blue-500" />;
    if (sensorName.includes("Light")) return <Sun className="h-4 w-4 text-yellow-500" />;
    if (sensorName.includes("Wind")) return <Wind className="h-4 w-4 text-gray-500" />;
    return <BarChart3 className="h-4 w-4 text-green-500" />;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Bar */}
      <nav className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link href="/agrotwin" className="flex items-center space-x-2 text-gray-700 hover:text-green-600 transition-colors">
                <Home className="h-5 w-5" />
                <span className="font-medium">Home</span>
              </Link>
              <div className="flex items-center space-x-2 text-green-600">
                <BarChart3 className="h-5 w-5" />
                <span className="font-semibold">Dashboard</span>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">Digital Twin Agriculture</span>
              <Link href="/agrotwin/settings" className="p-2 text-gray-500 hover:text-gray-700 transition-colors">
                <Settings className="h-5 w-5" />
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold mb-6">Digital Twin Dashboard (India)</h1>
        
        <div className="mb-8">
          {/* Summary Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white rounded shadow p-4">
              <div className="text-lg font-semibold">Farms</div>
              <div className="text-2xl">{mockFarms.length}</div>
            </div>
            <div className="bg-white rounded shadow p-4">
              <div className="text-lg font-semibold">Crops</div>
              <div className="text-2xl">15</div>
            </div>
            <div className="bg-white rounded shadow p-4">
              <div className="text-lg font-semibold">Sensors</div>
              <div className="text-2xl">38</div>
            </div>
            <div className="bg-white rounded shadow p-4">
              <div className="text-lg font-semibold">Actions</div>
              <div className="text-2xl">24</div>
            </div>
          </div>
        </div>

        {/* Live Sensor Monitoring */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold">🌡️ Live Sensor Monitoring</h2>
            <div className="flex items-center gap-2">
              <label htmlFor="farm-select" className="text-sm text-gray-600">Farm:</label>
              <select
                id="farm-select"
                value={selectedFarmId}
                onChange={e => setSelectedFarmId(e.target.value)}
                className="border rounded px-2 py-1 text-sm"
              >
                {mockFarms.map(farm => (
                  <option key={farm.id} value={farm.id}>
                    {farm.name} ({farm.state})
                  </option>
                ))}
              </select>
              <span className="text-sm text-gray-600 ml-2">Refresh:</span>
              <select
                value={refreshInterval}
                onChange={e => setRefreshInterval(Number(e.target.value))}
                className="border rounded px-2 py-1 text-sm"
              >
                <option value={2000}>2s</option>
                <option value={5000}>5s</option>
                <option value={10000}>10s</option>
                <option value={30000}>30s</option>
              </select>
            </div>
          </div>
          
          <div className="bg-white rounded shadow p-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {liveReadings.map((reading) => (
                <div key={reading.id} className="border rounded p-3 bg-gradient-to-r from-green-50 to-blue-50">
                  <div className="flex justify-between items-start">
                    <div className="flex items-center gap-2">
                      {getSensorIcon(reading.sensor.name)}
                      <div>
                        <div className="font-semibold text-sm">{reading.sensor.name}</div>
                        <div className="text-xs text-gray-600">
                          {reading.plot.farm.name} - {reading.plot.farm.state}
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold text-blue-600">
                        {reading.value.toFixed(1)} {reading.unit}
                      </div>
                      <div className="text-xs text-gray-500">
                        {reading.timestamp.toLocaleTimeString()}
                      </div>
                    </div>
                  </div>
                  <div className="mt-2 text-xs text-gray-500">
                    Plot: {reading.plot.crop?.name || 'Unknown Crop'}
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4 text-center text-sm text-gray-600">
              🔄 Live data updates every {refreshInterval / 1000}s • Last update: {lastUpdate.toLocaleTimeString()}
            </div>
          </div>
        </div>

        <h2 className="text-2xl font-bold mb-4">Farms</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {mockFarms.map((farm) => (
            <Link key={farm.id} href={`/agrotwin/farm/${farm.id}`} className="block">
              <div className="bg-white rounded shadow p-4 hover:shadow-lg transition-shadow cursor-pointer border border-transparent hover:border-green-200">
                <div className="text-xl font-semibold mb-2">{farm.name}</div>
                <div className="text-gray-600">{farm.state}, {farm.district}</div>
                <div className="mt-2 text-sm text-gray-500">
                  Plots: {farm.plots} | Sensors: {farm.sensors}
                </div>
                <div className="mt-3 text-sm text-green-600 font-medium">
                  View Details →
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage; 