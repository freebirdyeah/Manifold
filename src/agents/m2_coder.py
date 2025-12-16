import os
import json
import re
from src.utils.llm import call_llm

def run_coder(input_path: str, output_dir: str):
    """
    M2 Agent: Scene Intent JSON -> Manim Code (Python files)
    """
    # 1. Read Intents
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        scenes = data.get("scenes", [])
        
    # 2. Read System Prompt
    prompt_path = os.path.join("prompts", "m2_system.md")
    with open(prompt_path, 'r', encoding='utf-8') as f:
        system_prompt = f.read()
        
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Generating code for {len(scenes)} scenes from {input_path}...")
    
    for i, scene_data in enumerate(scenes):
        scene_id = scene_data.get("scene_id", f"scene_{i:02d}")
        
        print(f"  Generating {scene_id}...")
        
        user_prompt = f"Generate Manim code for this scene:\n\n{json.dumps(scene_data, indent=2)}"
        
        code = call_llm(system_prompt, user_prompt, json_mode=False)
        
        # Clean up markdown code blocks if present
        code = clean_code(code)
        
        # Validate: refuse to write empty or invalid files
        if not code or len(code.strip()) < 10:
            raise ValueError(f"LLM returned empty or invalid code for {scene_id}. Raw response length: {len(code) if code else 0}")
        
        if "class" not in code and "Scene" not in code:
            raise ValueError(f"LLM response for {scene_id} does not contain a Scene class definition. This file would be unrenderable.")
        
        # Save file
        # Ensure filename is safe
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', scene_id)
        file_path = os.path.join(output_dir, f"{safe_name}.py")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
            
    print(f"Code generation complete. Files saved in {output_dir}")

def clean_code(text: str) -> str:
    """Removes markdown code fences."""
    pattern = r"```python\s*(.*?)\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    
    pattern_generic = r"```\s*(.*?)\s*```"
    match_generic = re.search(pattern_generic, text, re.DOTALL)
    if match_generic:
        return match_generic.group(1)
        
    return text
