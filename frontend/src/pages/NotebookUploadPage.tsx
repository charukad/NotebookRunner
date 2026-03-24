import { useState } from 'react';
import { UploadCloud, Play, Settings } from 'lucide-react';

export default function NotebookUploadPage() {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [useGpu, setUseGpu] = useState(true);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold font-sans mb-2 text-white">Execute Notebook</h1>
      <p className="text-gray-400 mb-8">Upload an .ipynb file to patch, orchestrate, and run on Colab.</p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-2 space-y-6">
          <div 
            className={`border-2 border-dashed rounded-xl p-12 flex flex-col items-center justify-center transition ${dragActive ? 'border-blue-500 bg-blue-900/20' : 'border-gray-600 bg-gray-800 hover:border-gray-500'}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <UploadCloud size={48} className="text-gray-400 mb-4" />
            <p className="text-lg font-medium text-white">Drag & drop your notebook here</p>
            <p className="text-sm text-gray-400 mt-2">or click to browse (.ipynb only)</p>
            {file && <div className="mt-4 px-4 py-2 bg-gray-700 rounded-lg text-emerald-400 font-mono text-sm">{file.name}</div>}
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-gray-800 border border-gray-700 rounded-xl p-6">
            <h3 className="text-lg font-semibold flex items-center space-x-2 mb-4 text-white">
              <Settings size={20} className="text-gray-400"/>
              <span>Configuration</span>
            </h3>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Target Backend</span>
                <span className="text-white font-medium">Google Colab</span>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Require GPU</span>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" className="sr-only peer" checked={useGpu} onChange={() => setUseGpu(!useGpu)} />
                  <div className="w-11 h-6 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
              
            </div>

            <button disabled={!file} className="w-full mt-6 bg-emerald-600 hover:bg-emerald-500 disabled:bg-gray-700 disabled:text-gray-500 text-white font-medium py-3 rounded-lg flex items-center justify-center space-x-2 transition">
              <Play size={20} />
              <span>Launch Execution</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
