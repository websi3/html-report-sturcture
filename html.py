import json
from html import escape

with open("summary/tools-summary.json") as f:
    data = json.load(f)

html = f"<html><head><meta charset='utf-8'><title>Project Report</title></head><body>"
html += f"<h1>Project Report: {escape(data.get('project','unknown'))}</h1>"
html += "<h2>Tools Summary</h2><table border='1' cellpadding='5' cellspacing='0'>"
html += "<tr><th>Tool</th><th>Run ID</th><th>Domain/Target</th><th>Timestamp</th><th>Files</th></tr>"

for t in data["tools"]:
    html += "<tr>"
    html += f"<td>{escape(str(t.get('workflow','?')))}</td>"
    html += f"<td>{escape(str(t.get('run_id','?')))}</td>"
    html += f"<td>{escape(str(t.get('domain', t.get('target','?'))))}</td>"
    html += f"<td>{escape(str(t.get('timestamp','?')))}</td>"
    html += f"<td>{escape(str(t.get('file_count','?')))}</td>"
    html += "</tr>"

html += "</table></body></html>"

with open("project-reports/project-report.html", "w", encoding="utf-8") as f:
    f.write(html)
