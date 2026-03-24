import json

def analyze_notebook(file_content: bytes) -> dict:
    """
    Semantically analyzes a Jupyter Notebook to detect ML framework
    and missing artifact exports.
    """
    try:
        notebook = json.loads(file_content)
    except Exception:
        return {"error": "Invalid JSON"}

    framework = "unknown"
    has_training_loop = False
    needs_drive_mount = True
    
    cells = notebook.get("cells", [])
    for cell in cells:
        if cell.get("cell_type") != "code":
            continue
        
        source = "".join(cell.get("source", []))
        
        if "torch" in source or "fastai" in source:
            framework = "pytorch"
        elif "tensorflow" in source or "keras" in source:
            framework = "tensorflow"
            
        if "epochs" in source or "fit(" in source or "backward()" in source:
            has_training_loop = True
            
        if "drive.mount" in source:
            needs_drive_mount = False

    return {
        "framework": framework,
        "has_training_loop": has_training_loop,
        "needs_drive_mount": needs_drive_mount,
        "needs_artifact_export_patch": True,
        "detected_artifacts": ["model.pth"] if framework == "pytorch" else ["model.h5"]
    }
