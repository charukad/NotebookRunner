import { useEffect, useState } from 'react';
import { useProjectStore } from '../store/projectStore';
import { Folder, Plus } from 'lucide-react';

export default function ProjectsPage() {
  const { projects, setProjects } = useProjectStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setProjects([
        { id: '101', workspace_id: '1', name: 'Llama-3 Fine-tuning', description: 'LoRA fine-tuning on custom dataset' },
        { id: '102', workspace_id: '1', name: 'Stable Diffusion Generation', description: 'Image generation pipeline' }
      ]);
      setLoading(false);
    }, 500);
  }, []);

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold font-sans">Projects</h1>
          <p className="text-gray-400 mt-1">Organize your notebook jobs</p>
        </div>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition">
          <Plus size={20} />
          <span>New Project</span>
        </button>
      </div>

      {loading ? (
        <div className="text-gray-400">Loading projects...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {projects.map((p) => (
            <div key={p.id} className="bg-gray-800 border border-gray-700 rounded-xl p-6 hover:border-indigo-500 transition cursor-pointer">
               <div className="flex items-center space-x-3 mb-4">
                  <div className="p-3 bg-indigo-900/50 rounded-lg text-indigo-400">
                    <Folder size={24} />
                  </div>
                  <h3 className="text-xl font-semibold text-white">{p.name}</h3>
                </div>
                <p className="text-gray-400 text-sm">{p.description}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
