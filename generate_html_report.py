import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

# --- Configuration ---
INPUT_JSON_PATH = "summary/tools-summary.json"
OUTPUT_HTML_PATH = "project-reports/project-report.html"
# ---------------------

def flatten_tools(tools):
    """Flatten nested lists of tool dictionaries."""
    result = []
    for item in tools:
        if isinstance(item, list):
            result.extend(flatten_tools(item))
        elif isinstance(item, dict):
            result.append(item)
    return result

def generate_html_report():
    # Check if input file exists
    if not os.path.exists(INPUT_JSON_PATH):
        print(f"Error: Input file not found at '{INPUT_JSON_PATH}'")
        sys.exit(1)

    # Ensure output directory exists
    output_dir = os.path.dirname(OUTPUT_HTML_PATH)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"Created output directory: '{output_dir}'")

    try:
        # Load JSON data
        with open(INPUT_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

        project_name = data.get('project', 'N/A Project')
        target = data.get('target', 'N/A')
        date_str = datetime.now(timezone.utc).strftime("%d %b %Y")

        tools = flatten_tools(data.get("tools", []))

        # Workflow table
        workflow_rows = ""
        for t in tools:
            workflow = t.get("workflow", "N/A")
            run_id = t.get("run_id", "N/A")
            domain = t.get("domain", "N/A")
            timestamp = t.get("timestamp", "N/A")
            file_count = t.get("file_count", "N/A")
            workflow_rows += f"<tr><td>{workflow}</td><td>{run_id}</td><td>{domain}</td><td>{timestamp}</td><td>{file_count}</td></tr>"

        # Vulnerabilities
        vulnerabilities = data.get("vulnerabilities", {})
        vuln_html = ""
        for k, issues in vulnerabilities.items():
            vuln_html += f"<h4>{k}</h4><ul>"
            for i in issues:
                vuln_html += f"<li>{i}</li>"
            vuln_html += "</ul>"

        # Subdomains
        subdomains = data.get("subdomains", [])
        subdomain_rows = ""
        for s in subdomains:
            name = s.get("name", "N/A")
            status = s.get("status", "N/A")
            subdomain_rows += f"<tr><td>{name}</td><td>{status}</td></tr>"

        # Findings
        findings = data.get("findings", [])
        findings_html = "<ul>"
        for f in findings:
            findings_html += f"<li>{f}</li>"
        findings_html += "</ul>"

        # Fingerprint
        fingerprint = data.get("fingerprint", {})
        fingerprint_rows = ""
        for k, v in fingerprint.items():
            fingerprint_rows += f"<tr><td>{k}</td><td>{v}</td></tr>"

        # Notes
        notes = data.get("notes", [])
        notes_html = "<ul>"
        for n in notes:
            notes_html += f"<li>{n}</li>"
        notes_html += "</ul>"

        # CSS styling
        css = """
        <style>
        body { font-family: Arial, sans-serif; background:#0f1724; color:#e6eef8; padding:20px; }
        h1,h2 { color:#60a5fa; }
        table { width:100%; border-collapse: collapse; margin-bottom:20px; }
        th, td { border:1px solid #333; padding:8px; text-align:left; }
        th { background:#1e293b; }
        ul { margin:0; padding-left:20px; }
        .muted { color:#94a3b8; }
        .section { margin-bottom:30px; }
        </style>
        """

        # Combine HTML
        html = f"""
        <html>
        <head>
        <meta charset="utf-8">
        <title>Project Report: {project_name}</title>
        {css}
        </head>
        <body>
        <h1>Project Report: {project_name}</h1>
        <div class="muted">Target: {target}</div>
        <div class="muted">Date: {date_str}</div>

        <div class="section">
            <h2>1. Workflow Summary</h2>
            <table>
            <tr><th>Workflow</th><th>Run ID</th><th>Target / Domain</th><th>Timestamp</th><th>File Count</th></tr>
            {workflow_rows or '<tr><td colspan="5">No workflows found</td></tr>'}
            </table>
        </div>

        <div class="section">
            <h2>2. Vulnerabilities Detected</h2>
            {vuln_html or "<p>No vulnerabilities detected.</p>"}
        </div>

        <div class="section">
            <h2>3. Subdomain Discovery</h2>
            <table>
            <tr><th>Subdomain</th><th>Status</th></tr>
            {subdomain_rows or '<tr><td colspan="2">No subdomains found</td></tr>'}
            </table>
        </div>

        <div class="section">
            <h2>4. XSS / Other Findings</h2>
            {findings_html or "<p>No findings.</p>"}
        </div>

        <div class="section">
            <h2>5. Web Fingerprinting</h2>
            <table>
            {fingerprint_rows or '<tr><td colspan="2">No fingerprint data</td></tr>'}
            </table>
        </div>

        <div class="section">
            <h2>6. Notes on Workflow Outputs</h2>
            {notes_html or "<p>No notes.</p>"}
        </div>

        </body>
        </html>
        """

        Path(OUTPUT_HTML_PATH).write_text(html, encoding='utf-8')
        print(f"HTML report generated: '{OUTPUT_HTML_PATH}'")

    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{INPUT_JSON_PATH}'")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    generate_html_report()
