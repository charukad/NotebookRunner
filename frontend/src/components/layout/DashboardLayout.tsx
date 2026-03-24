import { Outlet, Link } from 'react-router-dom';
import { LayoutDashboard, Folder, PlayCircle, Settings } from 'lucide-react';

export default function DashboardLayout() {
  return (
    <div className="flex h-screen bg-gray-900 text-white font-sans">
      <aside className="w-64 bg-gray-800 border-r border-gray-700 flex flex-col">
        <div className="p-4 border-b border-gray-700">
          <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-500">
            Colab Runner
          </h1>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <Link to="/" className="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-700 transition">
            <LayoutDashboard size={20} className="text-blue-400" />
            <span>Workspaces</span>
          </Link>
          <Link to="/projects" className="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-700 transition">
            <Folder size={20} className="text-blue-400" />
            <span>Projects</span>
          </Link>
          <Link to="/notebooks/upload" className="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-700 transition">
            <PlayCircle size={20} className="text-blue-400" />
            <span>Execute</span>
          </Link>
        </nav>
        <div className="p-4 border-t border-gray-700">
          <button className="flex items-center space-x-3 w-full p-2 rounded-lg hover:bg-gray-700 transition">
            <Settings size={20} className="text-gray-400" />
            <span className="text-gray-400">Settings</span>
          </button>
        </div>
      </aside>
      <main className="flex-1 overflow-y-auto bg-gray-900">
        <div className="p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
