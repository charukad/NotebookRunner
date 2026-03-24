import { BrowserRouter, Routes, Route } from 'react-router-dom';
import DashboardLayout from './components/layout/DashboardLayout';
import WorkspacesPage from './pages/WorkspacesPage';
import ProjectsPage from './pages/ProjectsPage';
import NotebookUploadPage from './pages/NotebookUploadPage';
import JobMonitorPage from './pages/JobMonitorPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DashboardLayout />}>
          <Route index element={<WorkspacesPage />} />
          <Route path="projects" element={<ProjectsPage />} />
          <Route path="notebooks/upload" element={<NotebookUploadPage />} />
          <Route path="jobs/:jobId" element={<JobMonitorPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
