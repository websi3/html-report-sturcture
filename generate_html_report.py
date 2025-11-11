import json
import sys
from datetime import datetime

def generate_html_report(json_path, output_path):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    project = data.get("project", "Unknown Project")

    tools_data = data.get("tools", [])

    # 🔹 Flatten nested lists if needed
    flattened = []
    for t in tools_data:
        if isinstance(t, list):
            flattened.extend(t)
        else:
            flattened.append(t)

    html = f"""
    <html>
    <head>
        <meta charset='utf-8'>
        <title>Project Report - {project}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #fafafa; }}
            h1 {{ color: #2c3e50; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
            th {{ background-color: #e0e0e0; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
        </style>
    </head>
    <body>
        <h1> Project Report: {project}</h1>
        <p><b>Generated on:</b> {datetime.utcnow().isoformat()} UTC</p>
        <h2> Tools Summary</h2>
        <table>
            <tr>
                <th>Workflow</th>
                <th>Run ID</th>
                <th>Domain</th>
                <th>Timestamp</th>
                <th>File Count</th>
            </tr>
    """

    if not flattened:
        html += "<tr><td colspan='5'><i>No tools data found</i></td></tr>"
    else:
        for tool in flattened:
            if isinstance(tool, dict):
                html += f"""
                <tr>
                    <td>{tool.get('workflow','')}</td>
                    <td>{tool.get('run_id','')}</td>
                    <td>{tool.get('domain','')}</td>
                    <td>{tool.get('timestamp','')}</td>
                    <td>{tool.get('file_count','')}</td>
                </tr>
                """

    html += """
        </table>
        <hr>
        <p> <i>HTML report generated successfully.</i></p>
    </body>
    </html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_html_report.py input.json output.html")
        sys.exit(1)

    generate_html_report(sys.argv[1], sys.argv[2])
