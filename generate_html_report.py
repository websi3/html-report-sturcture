import json
import sys

def generate_html_report(input_path, output_path):
    with open(input_path, 'r') as f:
        data = json.load(f)

    project_name = data.get("project", "Unknown Project")

    html = f"""
    <html>
    <head>
      <meta charset='utf-8'>
      <title>Project Report: {project_name}</title>
      <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #fafafa; }}
        h1 {{ color: #1a73e8; }}
        h2 {{ color: #333; }}
        ul {{ line-height: 1.6; }}
        li {{ margin-bottom: 6px; }}
        .classification {{ background: #fff; padding: 10px; border-radius: 8px; margin: 10px 0; }}
        a {{ color: #1a73e8; text-decoration: none; }}
      </style>
    </head>
    <body>
      <h1>Project Report: {project_name}</h1>
      <h2>Tools Summary</h2>
      <ul>
    """

    for tool in data.get("tools", []):
        html += f"<li><strong>{tool.get('workflow','')}</strong> — Run ID: {tool.get('run_id','')} | Domain: {tool.get('domain','')}</li>"

    html += "</ul>"

    if "classifications" in data:
        html += "<h2>Classifications</h2>"
        for cls in data["classifications"]:
            desc = cls.get("desc", "")
            ref = cls.get("ref", "")
            html += f"<div class='classification'><p>{desc}</p><p><a href='{ref}' target='_blank'>Reference</a></p></div>"

    html += "</body></html>"

    with open(output_path, 'w') as out:
        out.write(html)

    print(f" HTML report generated at {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_html_report.py <input.json> <output.html>")
        sys.exit(1)
    generate_html_report(sys.argv[1], sys.argv[2])
