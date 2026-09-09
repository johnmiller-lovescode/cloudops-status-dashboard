import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime, timezone

app = FastAPI()

websites = [
    {"name": "Google", "url": "https://www.google.com"},
    {"name": "GitHub", "url": "https://github.com"},
    {"name": "Amazon", "url": "https://www.amazon.com"},
]


@app.get("/", response_class=HTMLResponse)
def dashboard():

    results = []

    for website in websites:
        try:
            response = requests.get(
                website["url"],
                timeout=5,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            response_time = round(
                response.elapsed.total_seconds() * 1000
            )

            if response.status_code < 400:
                status = "Operational"
                status_class = "up"
            else:
                status = "Down"
                status_class = "down"

            results.append({
                "name": website["name"],
                "url": website["url"],
                "status": status,
                "status_class": status_class,
                "response_time": response_time
            })

        except requests.exceptions.RequestException:
            results.append({
                "name": website["name"],
                "url": website["url"],
                "status": "Down",
                "status_class": "down",
                "response_time": "-"
            })

    operational = sum(
        1 for result in results
        if result["status"] == "Operational"
    )

    rows = ""

    for result in results:
        rows += f"""
        <tr>
            <td>
                <div class="service-name">{result["name"]}</div>
                <div class="service-url">{result["url"]}</div>
            </td>

            <td>
                <span class="status {result["status_class"]}">
                    <span class="dot"></span>
                    {result["status"]}
                </span>
            </td>

            <td class="response">
                {result["response_time"]} ms
            </td>
        </tr>
        """

    checked_at = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>CloudOps Status Dashboard</title>

        <meta name="viewport"
              content="width=device-width, initial-scale=1">

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                background: #0b1120;
                color: #e5e7eb;
                font-family: -apple-system, BlinkMacSystemFont,
                             "Segoe UI", sans-serif;
            }}

            .container {{
                max-width: 1050px;
                margin: 0 auto;
                padding: 60px 25px;
            }}

            .header {{
                margin-bottom: 35px;
            }}

            h1 {{
                margin: 0;
                font-size: 36px;
                letter-spacing: -1px;
            }}

            .subtitle {{
                color: #94a3b8;
                margin-top: 8px;
            }}

            .summary {{
                background: #111827;
                border: 1px solid #1f2937;
                border-radius: 12px;
                padding: 20px 24px;
                margin-bottom: 25px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}

            .summary-title {{
                font-weight: 600;
            }}

            .summary-status {{
                color: #34d399;
                font-weight: 600;
            }}

            .card {{
                background: #111827;
                border: 1px solid #1f2937;
                border-radius: 12px;
                overflow: hidden;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            th {{
                text-align: left;
                color: #94a3b8;
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 1px;
                padding: 18px 22px;
                background: #0f172a;
            }}

            td {{
                padding: 22px;
                border-top: 1px solid #1f2937;
            }}

            .service-name {{
                font-weight: 600;
                margin-bottom: 4px;
            }}

            .service-url {{
                color: #64748b;
                font-size: 13px;
            }}

            .status {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                font-weight: 600;
            }}

            .dot {{
                width: 8px;
                height: 8px;
                border-radius: 50%;
                display: inline-block;
            }}

            .up {{
                color: #34d399;
            }}

            .up .dot {{
                background: #34d399;
            }}

            .down {{
                color: #f87171;
            }}

            .down .dot {{
                background: #f87171;
            }}

            .response {{
                font-family: monospace;
                font-size: 15px;
            }}

            .footer {{
                margin-top: 18px;
                color: #64748b;
                font-size: 13px;
                display: flex;
                justify-content: space-between;
            }}

            @media (max-width: 650px) {{

                .container {{
                    padding: 35px 15px;
                }}

                h1 {{
                    font-size: 28px;
                }}

                .service-url {{
                    display: none;
                }}

                td, th {{
                    padding: 16px 12px;
                }}
            }}

        </style>
    </head>

    <body>

        <div class="container">

            <div class="header">
                <h1>CloudOps Status Dashboard</h1>
                <div class="subtitle">
                    Automated cloud service health monitoring
                </div>
            </div>

            <div class="summary">

                <div>
                    <div class="summary-title">
                        System Status
                    </div>
                    <div class="subtitle">
                        {operational} of {len(results)} services operational
                    </div>
                </div>

                <div class="summary-status">
                    ● Monitoring Active
                </div>

            </div>

            <div class="card">

                <table>

                    <tr>
                        <th>Service</th>
                        <th>Status</th>
                        <th>Response Time</th>
                    </tr>

                    {rows}

                </table>

            </div>

            <div class="footer">
                <span>CloudOps Monitoring Platform</span>
                <span>Last checked: {checked_at}</span>
            </div>

        </div>

    </body>
    </html>
    """


@app.get("/health")
def health():
    return {"status": "healthy"}