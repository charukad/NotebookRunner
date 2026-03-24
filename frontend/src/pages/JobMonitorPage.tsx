import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Activity, Terminal, CheckCircle, Clock } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function JobMonitorPage() {
  const { jobId } = useParams();
  const [logs, setLogs] = useState<string[]>([]);
  const [metrics, setMetrics] = useState<any[]>([]);
  const [status, setStatus] = useState('running');

  useEffect(() => {
    // Mocking WebSocket live data stream
    const mockLogs = [
      "INFO: Connecting to Colab...",
      "INFO: Colab environment initialized.",
      "INFO: Downloading dataset...",
      "INFO: Starting training loop."
    ];
    
    let step = 0;
    const interval = setInterval(() => {
      if (step < mockLogs.length) {
        setLogs(prev => [...prev, mockLogs[step]]);
      }
      
      if (step > 2 && step < 20) {
        setMetrics(prev => [...prev, {
          step: prev.length,
          loss: Math.max(0.1, 2.5 * Math.exp(-0.1 * prev.length) + (Math.random() * 0.2))
        }]);
      } else if (step === 20) {
        setStatus('completed');
        setLogs(prev => [...prev, "INFO: Job completed successfully. Artifacts pushed to MinIO."]);
        clearInterval(interval);
      }
      step++;
    }, 1000);

    return () => clearInterval(interval);
  }, [jobId]);

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold font-sans text-white">Job Monitor</h1>
          <p className="text-gray-400 mt-1">ID: {jobId}</p>
        </div>
        
        <div className="flex items-center space-x-2 bg-gray-800 px-4 py-2 rounded-lg border border-gray-700">
          {status === 'running' ? (
             <><Activity className="text-blue-500 animate-pulse" size={20} /><span className="text-blue-400 font-medium tracking-wide">RUNNING</span></>
          ) : (
             <><CheckCircle className="text-emerald-500" size={20} /><span className="text-emerald-400 font-medium tracking-wide">COMPLETED</span></>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Terminal Logs */}
        <div className="bg-gray-950 border border-gray-700 rounded-xl overflow-hidden flex flex-col h-96">
          <div className="bg-gray-800 p-3 border-b border-gray-700 flex items-center space-x-2">
            <Terminal size={18} className="text-gray-400" />
            <span className="text-gray-300 font-mono text-sm">Live Logs</span>
          </div>
          <div className="p-4 overflow-y-auto flex-1 font-mono text-sm text-green-400 space-y-1">
            {logs.map((log, i) => (
              <div key={i}>{log}</div>
            ))}
            {status === 'running' && (
              <div className="flex items-center space-x-2 text-gray-500 mt-4">
                <Clock className="animate-spin" size={14} />
                <span>Waiting for output...</span>
              </div>
            )}
          </div>
        </div>

        {/* Metrics Chart */}
        <div className="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden flex flex-col h-96">
          <div className="bg-gray-800 p-3 border-b border-gray-700">
            <span className="text-gray-300 font-medium text-sm">Training Loss</span>
          </div>
          <div className="p-4 flex-1">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={metrics}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="step" stroke="#9CA3AF" />
                <YAxis stroke="#9CA3AF" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1F2937', border: 'none', borderRadius: '8px', color: '#fff' }}
                  itemStyle={{ color: '#60A5FA' }}
                />
                <Line type="monotone" dataKey="loss" stroke="#3B82F6" strokeWidth={2} dot={false} isAnimationActive={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
