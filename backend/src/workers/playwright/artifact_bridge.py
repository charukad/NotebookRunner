import os
from src.infrastructure.storage.minio_client import get_minio_client

class ArtifactBridge:
    """
    Downloads artifacts exported to Google Drive (which synced locally on host if Drive Desktop is running)
    or downloads them directly via browser automation, then uploads to MinIO.
    """
    
    def __init__(self, page):
        self.page = page
        self.minio = get_minio_client()

    async def collect_from_browser(self, job_id: str, artifact_paths: list):
        """Fallback: uses the Playwright page.download behavior to pull files from Colab file pane."""
        # Colab file viewer is complex, so injecting shutil into notebook is much better.
        pass
        
    def sync_to_registry(self, job_id: str, local_export_dir: str):
        """Scans the local export dir and pushes everything to MinIO jobs bucket."""
        if not os.path.exists(local_export_dir):
            raise FileNotFoundError("Local export directory missing")
            
        bucket_name = "job-artifacts"
        if not self.minio.bucket_exists(bucket_name):
            self.minio.make_bucket(bucket_name)
            
        uploaded_artifacts = []
        for file in os.listdir(local_export_dir):
            file_path = os.path.join(local_export_dir, file)
            if os.path.isfile(file_path):
                dest_name = f"{job_id}/{file}"
                self.minio.fput_object(bucket_name, dest_name, file_path)
                uploaded_artifacts.append(dest_name)
                
        return uploaded_artifacts
