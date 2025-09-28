import os
# Input and output file paths
input_file = "seed_keywords.txt"
output_dir = "output"
output_file = os.path.join(output_dir, "ideas.txt")
# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)
# Read seed keywords
with open(input_file, "r") as f:
    seeds = [line.strip() for line in f if line.strip()]
# Generate ideas (simple expansion logic, replace with your own later)
ideas = []
for s in seeds:
    ideas.append(f"{s} automation ideas")
    ideas.append(f"{s} monetization strategies")
    ideas.append(f"Top 10 {s} use cases")
    ideas.append(f"{s} project starter templates")
# Write ideas to file
with open(output_file, "w") as f:
    f.write("\n".join(ideas))
print(f":white_tick: Generated {len(ideas)} ideas in {output_file}")
