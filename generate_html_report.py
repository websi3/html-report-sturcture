import json
import sys
from datetime import datetime

def generate_html_report(json_path, output_path):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    project = data.get("project", "Untitled Project")
    tools_data = data.get("tools", [])

    # flatten nested lists if needed
    flattened = []
    for t in tools_data:
        if isinstance(t, list):
            flattened.extend(t)
        else:
            flattened.append(t)

    timestamp = datetime.utcnow().isoformat() + "Z"

    css = """
    <style>
    :root {
        --bg: #0f1724;
        --card: #0b1220;
        --muted: #94a3b8;
        --accent: #60a5fa;
        --good: #10b981;
        --bad: #ef4444;
        --glass: rgba(255,255,255,0.05);
        --border: rgba(255,255,255,0.1);
    }
    body {
        background: linear-gradient(180deg,#071027 0%, #04111b 100%);
        color: #e6eef8;
        font-family: Inter,Segoe UI,Helvetica,Arial,sans-serif;
        padding: 24px;
    }
    .container {
        max-width: 950px;
        margin: 24px auto;
        padding: 24px;
        background: var(--card);
        border-radius: 14px;
        box-shadow: 0 6px 24px rgba(2,6,23,0.6);
    }
    h1 { color: var(--accent); margin-bottom: 4px; font-size: 26px; }
    .meta { color: var(--muted); margin-bottom: 12px; }
    .section {
        background: var(--glass);
        border-radius: 10px;
        padding: 16px;
        margin-top: 20px;
    }
    .tool-box {
        background: rgba(255,255,255,0.03);
        padding: 16px;
        border-radius: 10px;
        margin-bottom: 14px;
        border-left: 4px solid var(--accent);
        transition: all 0.2s ease;
    }
    .tool-box:hover {
        transform: scale(1.01);
        background: rgba(255,255,255,0.06);
    }
    .tool-header {
        font-weight: bold;
        color: var(--accent);
        font-size: 17px;
        margin-bottom: 6px;
    }
    .tool-info {
        color: var(--muted);
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 8px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 8px;
    }
    th, td {
        border: 1px solid var(--border);
        padding: 6px 8px;
        text-align: left;
        font-size: 13px;
    }
    th { background: rgba(255,255,255,0.08); color: var(--accent); }
    td { color: #dbeafe; }
    .footer {
        text-align: center;
        color: var(--muted);
        font-size: 13px;
        margin-top: 30px;
    }
    .no-data { color: var(--muted); font-style: italic; }
    </style>
    """

    header_html = f"""
    <header style='display:flex;align-items:center;gap:12px;margin-bottom:8px'>
        <div style='font-family:monospace;font-weight:700;color:#60a5fa;font-size:26px'>WEBSI3</div>
        <div style='color:#94a3b8;margin-left:8px;font-size:14px'>Vulnerability Scanner — Project Report</div>
    </header>
    """

    html = f"""
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <title>{project} - Report</title>
        {css}
    </head>
    <body>
        <div class="container">
            {header_html}
            <h1>Project Report: {project}</h1>
            <div class="meta">Generated on: {timestamp}</div>

            <div class="section">
                <h2>🧰 Tools Summary & Results</h2>
    """

    if not flattened:
        html += "<p class='no-data'>No tools data found.</p>"
    else:
        for i, tool in enumerate(flattened, start=1):
            if not isinstance(tool, dict):
                continue

            workflow = tool.get("workflow", "").strip()
            run_id = tool.get("run_id", "").strip()
            domain = tool.get("domain", "").strip()
            ts = tool.get("timestamp", "").strip()
            fc = tool.get("file_count", "").strip()

            # Skip tools with no valid data
            if not any([workflow, run_id, domain, ts, fc]):
                continue

            html += f"""
            <div class="tool-box">
                <div class="tool-header">#{i} — {workflow or "N/A"}</div>
                <div class="tool-info">
                    <b>Run ID:</b> {run_id or "N/A"}<br>
                    <b>Domain:</b> {domain or "N/A"}<br>
                    <b>Timestamp:</b> {ts or "N/A"}<br>
                    <b>File Count:</b> {fc or "N/A"}
                </div>
            """

            # show findings or vulnerabilities if present
            findings = tool.get("findings") or tool.get("vulnerabilities") or tool.get("results") or []
            if isinstance(findings, list) and findings:
                html += "<table><tr><th>#</th><th>Finding</th></tr>"
                for idx, fnd in enumerate(findings, 1):
                    if isinstance(fnd, dict):
                        desc = fnd.get("desc") or fnd.get("description") or json.dumps(fnd)
                    else:
                        desc = str(fnd)
                    html += f"<tr><td>{idx}</td><td>{desc}</td></tr>"
                html += "</table>"
            else:
                html += "<div class='no-data'>No findings reported for this tool.</div>"

            html += "</div>"

    html += """
            </div>
            <div class="footer">Generated by <b>Websi3</b> — All reports stored securely in S3</div>
        </div>
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
