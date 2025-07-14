"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowLeft, MapPin, Calendar, Thermometer, Droplets, Sun, Wind, BarChart3 } from "lucide-react";

// Mock farm data
const mockFarmData = {
  id: "1",
  name: "Green Valley Farm",
  state: "Punjab",
  district: "Amritsar",
  area: "25 acres",
  established: "2020",
  plots: [
    {
      id: "1",
      name: "Plot A",
      crop: "Wheat",
      area: "5 acres",
      status: "Growing",
      sensors: [
        { name: "Temperature", value: 28.5, unit: "°C", status: "normal" },
        { name: "Humidity", value: 65, unit: "%", status: "normal" },
        { name: "Soil Moisture", value: 42, unit: "%", status: "low" }
      ]
    },
    {
      id: "2",
      name: "Plot B", 
      crop: "Rice",
      area: "3 acres",
      status: "Growing",
      sensors: [
        { name: "Temperature", value: 26.8, unit: "°C", status: "normal" },
        { name: "Humidity", value: 78, unit: "%", status: "high" },
        { name: "Soil Moisture", value: 68, unit: "%", status: "normal" }
      ]
    }
  ]
};

const FarmDetailPage = ({ params }: { params: { id: string } }) => {
  const [farmData, setFarmData] = useState(mockFarmData);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  // Simulate live data updates
  useEffect(() => {
    const interval = setInterval(() => {
      setFarmData(prev => ({
        ...prev,
        plots: prev.plots.map(plot => ({
          ...plot,
          sensors: plot.sensors.map(sensor => ({
            ...sensor,
            value: sensor.value + (Math.random() - 0.5) * 2
          }))
        }))
      }));
      setLastUpdate(new Date());
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const getSensorIcon = (sensorName: string) => {
    if (sensorName.includes("Temperature")) return <Thermometer className="h-4 w-4 text-red-500" />;
    if (sensorName.includes("Humidity") || sensorName.includes("Moisture")) return <Droplets className="h-4 w-4 text-blue-500" />;
    if (sensorName.includes("Light")) return <Sun className="h-4 w-4 text-yellow-500" />;
    if (sensorName.includes("Wind")) return <Wind className="h-4 w-4 text-gray-500" />;
    return <BarChart3 className="h-4 w-4 text-green-500" />;
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "normal": return "text-green-600";
      case "high": return "text-orange-600";
      case "low": return "text-red-600";
      default: return "text-gray-600";
    }
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
              <span className="text-sm text-gray-500">Digital Twin - {farmData.name}</span>
            </div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto py-8 px-4">
        {/* Farm Header */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{farmData.name}</h1>
              <div className="flex items-center space-x-4 mt-2 text-gray-600">
                <div className="flex items-center space-x-1">
                  <MapPin className="h-4 w-4" />
                  <span>{farmData.state}, {farmData.district}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Calendar className="h-4 w-4" />
                  <span>Est. {farmData.established}</span>
                </div>
              </div>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-green-600">{farmData.area}</div>
              <div className="text-sm text-gray-500">Total Area</div>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-green-50 rounded-lg p-4">
              <div className="text-lg font-semibold text-green-700">Plots</div>
              <div className="text-2xl font-bold">{farmData.plots.length}</div>
            </div>
            <div className="bg-blue-50 rounded-lg p-4">
              <div className="text-lg font-semibold text-blue-700">Active Sensors</div>
              <div className="text-2xl font-bold">
                {farmData.plots.reduce((total, plot) => total + plot.sensors.length, 0)}
              </div>
            </div>
            <div className="bg-orange-50 rounded-lg p-4">
              <div className="text-lg font-semibold text-orange-700">Crops</div>
              <div className="text-2xl font-bold">
                {new Set(farmData.plots.map(plot => plot.crop)).size}
              </div>
            </div>
          </div>
        </div>

        {/* Plots */}
        <h2 className="text-2xl font-bold mb-6">Farm Plots</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {farmData.plots.map((plot) => (
            <div key={plot.id} className="bg-white rounded-lg shadow p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-semibold">{plot.name}</h3>
                  <p className="text-gray-600">{plot.crop} • {plot.area}</p>
                  <span className="inline-block mt-2 px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                    {plot.status}
                  </span>
                </div>
              </div>

              <div className="space-y-3">
                <h4 className="font-medium text-gray-700">Sensor Readings</h4>
                {plot.sensors.map((sensor, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-2">
                      {getSensorIcon(sensor.name)}
                      <span className="font-medium">{sensor.name}</span>
                    </div>
                    <div className="text-right">
                      <div className={`font-bold ${getStatusColor(sensor.status)}`}>
                        {sensor.value.toFixed(1)} {sensor.unit}
                      </div>
                      <div className="text-xs text-gray-500 capitalize">{sensor.status}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-8 text-center text-sm text-gray-600">
          🔄 Live data updates every 5s • Last update: {lastUpdate.toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
};

export default FarmDetailPage; 