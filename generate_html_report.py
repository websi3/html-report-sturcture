import json
import os
import sys

# --- Configuration ---
INPUT_JSON_PATH = "summary/tools-summary.json"
OUTPUT_HTML_PATH = "project-reports/project-report.html"
# ---------------------

def generate_html_report():
    # Ensure input file exists
    if not os.path.exists(INPUT_JSON_PATH):
        print(f"Error: Input file not found at '{INPUT_JSON_PATH}'")
        sys.exit(1)

    # Ensure output directory exists
    output_dir = os.path.dirname(OUTPUT_HTML_PATH)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"Created output directory: '{output_dir}'")

    try:
        # Read JSON data
        with open(INPUT_JSON_PATH, "r") as f:
            data = json.load(f)

        project_name = data.get("project", "Unnamed Project")
        tools_list = data.get("tools", [])

        # HTML header + simple CSS
        html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Project Report: {project_name}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #f8f9fa;
                    margin: 20px;
                }}
                h1 {{
                    color: #333;
                }}
                .tool {{
                    background: #fff;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    margin: 10px 0;
                    padding: 10px;
                }}
                pre {{
                    background: #f1f1f1;
                    padding: 8px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
            </style>
        </head>
        <body>
            <h1>Project Report: {project_name}</h1>
        """

        if not tools_list:
            html += "<p><i>No tools data found.</i></p>"
        else:
            for i, tool in enumerate(tools_list, 1):
                html += f"<div class='tool'><h2>Tool #{i}</h2><pre>{json.dumps(tool, indent=4)}</pre></div>"

        html += """
        </body>
        </html>
        """

        # Write formatted HTML
        with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as html_file:
            html_file.write(html)

        print(f" Successfully generated HTML report: '{OUTPUT_HTML_PATH}'")

    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{INPUT_JSON_PATH}'. Check file format.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    generate_html_report()
