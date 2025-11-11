import json
from datetime import datetime
from pathlib import Path

def generate_html_report(json_path: str, output_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    project = data.get("project", "Untitled Project")
    target = data.get("target", "N/A")
    report_date = data.get("date", datetime.utcnow().strftime("%d %b %Y"))

    workflows = data.get("workflows", [])
    vulnerabilities = data.get("vulnerabilities", [])
    subdomains = data.get("subdomains", [])
    findings = data.get("findings", [])
    fingerprint = data.get("fingerprint", [])
    notes = data.get("notes", [])

    css = """
    <style>
      body { font-family: Arial, sans-serif; background-color:#f4f4f4; color:#111; margin:20px; }
      h1, h2, h3 { color:#1f2937; }
      table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
      th, td { border: 1px solid #ccc; padding: 8px; text-align:left; }
      th { background-color: #e5e7eb; }
      .section { margin-bottom: 30px; }
      .subdomain-list, .finding-list, .fingerprint-list, .notes-list { margin-left:20px; }
    </style>
    """

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Project Report: {project}</title>
      {css}
    </head>
    <body>
      <h1>Project Report: {project}</h1>
      <p><b>Target:</b> {target}</p>
      <p><b>Date:</b> {report_date}</p>

      <div class="section">
        <h2>1. Workflow Summary</h2>
        <table>
          <tr>
            <th>Workflow</th>
            <th>Run ID</th>
            <th>Target / Domain</th>
            <th>Timestamp</th>
            <th>File Count</th>
          </tr>
    """
    for wf in workflows:
        html += f"""
          <tr>
            <td>{wf.get('workflow', '')}</td>
            <td>{wf.get('run_id', '')}</td>
            <td>{wf.get('domain', '')}</td>
            <td>{wf.get('timestamp', '')}</td>
            <td>{wf.get('file_count', '')}</td>
          </tr>
        """
    html += "</table></div>"

    # Vulnerabilities Section
    html += '<div class="section"><h2>2. Vulnerabilities Detected</h2>'
    for vuln in vulnerabilities:
        html += f"<h3>{vuln.get('title')}</h3><ul>"
        for item in vuln.get("issues", []):
            html += f"<li>{item}</li>"
        html += "</ul>"
    html += "</div>"

    # Subdomains
    html += '<div class="section"><h2>3. Subdomain Discovery</h2><ul class="subdomain-list">'
    for sub in subdomains:
        html += f"<li>{sub.get('name')} — {sub.get('status')}</li>"
    html += "</ul></div>"

    # Findings
    html += '<div class="section"><h2>4. XSS / Other Findings</h2><ul class="finding-list">'
    for f in findings:
        html += f"<li>{f}</li>"
    html += "</ul></div>"

    # Fingerprint
    html += '<div class="section"><h2>5. Web Fingerprinting</h2><ul class="fingerprint-list">'
    for fp in fingerprint:
        html += f"<li>{fp}</li>"
    html += "</ul></div>"

    # Notes
    html += '<div class="section"><h2>6. Notes on Workflow Outputs</h2><ul class="notes-list">'
    for n in notes:
        html += f"<li>{n}</li>"
    html += "</ul></div>"

    html += """
    </body>
    </html>
    """

    Path(output_path).write_text(html, encoding="utf-8")
    print(f"HTML report generated: {output_path}")

# Example usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python generate_html_report.py <input_json> <output_html>")
        sys.exit(1)
    generate_html_report(sys.argv[1], sys.argv[2])
