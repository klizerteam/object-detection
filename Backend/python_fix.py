import os

Dataset_dir = "window_dataset"

CLASS_MAP = {
    "0": "2",   
    "1": "5"    
}

splits = ["train", "valid", "test"]
total = 0

for split in splits:
    labels_path = os.path.join(Dataset_dir, split, "labels")
    if not os.path.exists(labels_path):
        print(f"Missing: {labels_path}")
        continue

    for file in os.listdir(labels_path):
        if not file.endswith(".txt"):
            continue

        file_path = os.path.join(labels_path, file)

        with open(file_path, "r") as f:
            lines = f.readlines()

        new_lines = []
        changed = False

        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue

            
            if parts[0] in CLASS_MAP:
                parts[0] = CLASS_MAP[parts[0]]
                changed = True

            new_lines.append(" ".join(parts))

        if changed:
            total += 1
            with open(file_path, "w") as f:
                f.write("\n".join(new_lines))

print(f"Updated {total} label files (0→2, 1→5)")
