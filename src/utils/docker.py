import subprocess
import os

def run_in_docker(scene_file_path: str, output_dir: str):
    """
    Runs the manim render command inside the docker container.
    
    Args:
        scene_file_path: Absolute path to the python scene file on HOST.
        output_dir: Absolute path to the media output directory on HOST.
    """
    
    # We need to map the workspace root to /workspace in the container
    # Assuming the structure is Manifold/workspace/...
    
    # Find the workspace root (parent of 'code' folder)
    # scene_file_path is like .../Manifold/workspace/code/scene_01.py
    
    code_dir = os.path.dirname(scene_file_path)
    workspace_root = os.path.dirname(code_dir) # .../Manifold/workspace
    
    # The file path inside docker will be /workspace/code/filename.py
    filename = os.path.basename(scene_file_path)
    docker_file_path = f"/workspace/code/{filename}"

    # Ensure the host output dir exists (it's mounted into /workspace/media).
    os.makedirs(output_dir, exist_ok=True)
    docker_media_dir = "/workspace/media"

    # Default to the same image as docker-compose.yml.
    # Can be overridden by setting MANIFOLD_DOCKER_IMAGE.
    docker_image = os.environ.get("MANIFOLD_DOCKER_IMAGE", "manimcommunity/manim:stable")
    
    # Construct the docker command
    # docker run --rm -v /host/path/to/workspace:/workspace manimcommunity/manim:v0.18.1 manim -qm /workspace/code/scene.py
    
    # On Windows/WSL, paths might need adjustment, but usually absolute paths work if in WSL.
    
    cmd = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{workspace_root}:/workspace",
        "-w",
        "/workspace",
        docker_image,
        "manim",
        "-qm",
        "-a",
        "--disable_caching",
        "--media_dir",
        docker_media_dir,
        docker_file_path,
    ]
    
    print(f"Running Docker command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Render successful.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Render failed.")
        print(e.stderr)
        print(e.stdout)
        raise e
