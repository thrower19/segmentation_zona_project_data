from pathlib import Path

transformed_dir = Path("/local/scratch/segmentation_zona_project_data/transformed")

for fcsv_file in transformed_dir.glob("*.fcsv"):
    lines = fcsv_file.read_text().splitlines()

    header_lines = []
    data_lines = []

    for line in lines:
        if line.startswith("#"):
            header_lines.append(line)
        elif line.strip():
            data_lines.append(line.split(","))

    # Find the rows by label (column index 11 is 'label')
    r_row = next((row for row in data_lines if row[11].strip() == "r_cZi"), None)
    l_row = next((row for row in data_lines if row[11].strip() == "l_cZi"), None)

    if r_row and l_row:
        # Re-assign IDs (column index 0) so the top row is 1 and the second row is 2
        r_row[0] = "1"
        l_row[0] = "2"

        # Combine reordered rows and any remaining rows
        other_rows = [
            row
            for row in data_lines
            if row[11].strip() not in ("r_cZi", "l_cZi")
        ]
        reordered_data = [r_row, l_row] + other_rows

        # Format rows back to CSV strings
        new_content = "\n".join(
            header_lines + [",".join(row) for row in reordered_data]
        )

        fcsv_file.write_text(new_content + "\n")
        print(f"Updated: {fcsv_file.name}")
