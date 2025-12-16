import argparse
import os
import sys
from src.agents.m1_planner import run_planner
from src.agents.m2_coder import run_coder
from src.utils.docker import run_in_docker

def main():
    parser = argparse.ArgumentParser(description="Manifold: Text to Video Agent")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Command: plan
    plan_parser = subparsers.add_parser("plan", help="M1: Text -> JSON")
    plan_parser.add_argument("input_file", help="Path to text file")
    
    # Command: gen
    gen_parser = subparsers.add_parser("gen", help="M2: JSON -> Python Code")
    gen_parser.add_argument("input_file", help="Path to JSON file")
    
    # Command: render
    render_parser = subparsers.add_parser("render", help="Render a scene file in Docker")
    render_parser.add_argument("scene_file", help="Path to Python scene file")
    
    args = parser.parse_args()
    
    # Define workspace paths
    base_dir = os.getcwd()
    workspace_dir = os.path.join(base_dir, "workspace")
    intents_dir = os.path.join(workspace_dir, "intents")
    code_dir = os.path.join(workspace_dir, "code")
    media_dir = os.path.join(workspace_dir, "media")
    
    if args.command == "plan":
        run_planner(args.input_file, intents_dir)
        
    elif args.command == "gen":
        run_coder(args.input_file, code_dir)
        
    elif args.command == "render":
        # Ensure absolute path
        scene_path = os.path.abspath(args.scene_file)
        run_in_docker(scene_path, media_dir)
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
