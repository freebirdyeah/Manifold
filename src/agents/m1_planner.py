import os
import json
from src.utils.llm import call_llm

def run_planner(input_path: str, output_dir: str):
    """
    M1 Agent: Text -> Scene Intent JSON
    """
    # 1. Read Input
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()
        
    # 2. Read System Prompt
    prompt_path = os.path.join("prompts", "m1_system.md")
    with open(prompt_path, 'r', encoding='utf-8') as f:
        system_prompt = f.read()
        
    print(f"Planning scenes for: {input_path}...")
    
    # 3. Call LLM
    # We ask for JSON mode to ensure valid parsing.
    # We want a single JSON object with a "scenes" key.
    
    user_prompt = f"Here is the manuscript:\n\n{raw_text}\n\nPlease generate the scene intents as a JSON object with a 'scenes' list."
    
    response = call_llm(system_prompt, user_prompt, json_mode=True)
    print(response)
    
    try:
        data = json.loads(response)
        scenes = data.get("scenes", [])
        print(scenes)
    except json.JSONDecodeError:
        print("Error: LLM did not return valid JSON.")
        return

    # 4. Save to JSON
    filename = os.path.basename(input_path).replace(".txt", ".json")
    output_path = os.path.join(output_dir, filename)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the entire data object (which contains the list of scenes)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
            
    print(f"Generated {len(scenes)} scenes in {output_path}")
