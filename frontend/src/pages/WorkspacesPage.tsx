import { useEffect, useState } from 'react';
import { useWorkspaceStore } from '../store/workspaceStore';
import { LayoutDashboard, Plus } from 'lucide-react';

export default function WorkspacesPage() {
  const { workspaces, setWorkspaces } = useWorkspaceStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setWorkspaces([
        { id: '1', name: 'Personal Workspace', plan: 'free' },
        { id: '2', name: 'Team Alpha', plan: 'pro' }
      ]);
      setLoading(false);
    }, 500);
  }, []);

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold font-sans">Workspaces</h1>
          <p className="text-gray-400 mt-1">Manage your Colab execution environments</p>
        </div>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition">
          <Plus size={20} />
          <span>New Workspace</span>
        </button>
      </div>

      {loading ? (
        <div className="animate-pulse flex space-x-4">
          <div className="flex-1 space-y-4 py-1">
            <div className="h-4 bg-gray-700 rounded w-3/4"></div>
            <div className="space-y-2">
              <div className="h-4 bg-gray-700 rounded"></div>
              <div className="h-4 bg-gray-700 rounded w-5/6"></div>
            </div>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {workspaces.map((ws) => (
            <div key={ws.id} className="bg-gray-800 border border-gray-700 rounded-xl p-6 hover:border-blue-500 transition cursor-pointer flex flex-col justify-between h-40">
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-3 bg-blue-900/50 rounded-lg text-blue-400">
                    <LayoutDashboard size={24} />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-white">{ws.name}</h3>
                    <span className="text-xs px-2 py-1 bg-gray-700 text-gray-300 rounded-full mt-2 inline-block capitalize">{ws.plan} Plan</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
