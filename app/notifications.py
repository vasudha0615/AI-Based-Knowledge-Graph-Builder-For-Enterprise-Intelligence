"""
notifications.py — Slack & Email Notification System
Sends daily metric summaries via Slack webhook and email.
"""

import smtplib
import json
import urllib.request
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ── Configuration ──────────────────────────────────
# Replace these with your actual credentials

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

EMAIL_SENDER    = "your_email@gmail.com"
EMAIL_PASSWORD  = "your_app_password"       # Gmail App Password
EMAIL_RECEIVER  = "receiver@gmail.com"

# ══════════════════════════════════════════════════
# SLACK NOTIFICATION
# ══════════════════════════════════════════════════
def send_slack_summary(stats):
    """
    Sends a daily metrics summary to a Slack channel via webhook.

    stats = {
        "total_queries":     50,
        "avg_response_time": 1234.5,
        "avg_similarity":    0.87,
        "cache_hit_rate":    23.5,
        "total_tokens_used": 12500
    }
    """

    # Build the Slack message with blocks for rich formatting
    message = {
        "text": "📊 *KGB Daily Metrics Summary*",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🧠 KGB — Daily Intelligence Report"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Date:* {datetime.datetime.utcnow().strftime('%Y-%m-%d')}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Total Queries:*\n{stats.get('total_queries', 0)}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Avg Response Time:*\n{stats.get('avg_response_time', 0):.1f} ms"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Avg Similarity Score:*\n{stats.get('avg_similarity', 0):.4f}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Cache Hit Rate:*\n{stats.get('cache_hit_rate', 0):.1f}%"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Total Tokens Used:*\n{stats.get('total_tokens_used', 0):,}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Model:*\nMistral 7B"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "_Powered by KGB Enterprise Intelligence Platform_"
                }
            }
        ]
    }

    # Send POST request to Slack webhook
    try:
        data = json.dumps(message).encode('utf-8')
        req  = urllib.request.Request(
            SLACK_WEBHOOK_URL,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        urllib.request.urlopen(req)
        print("✅ Slack notification sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Slack notification failed: {e}")
        return False


# ══════════════════════════════════════════════════
# EMAIL NOTIFICATION
# ══════════════════════════════════════════════════
def send_email_summary(stats):
    """
    Sends a daily metrics summary via email using smtplib.
    Uses Gmail SMTP server with App Password authentication.
    """

    # Build email subject and body
    subject = f"📊 KGB Daily Metrics — {datetime.datetime.utcnow().strftime('%Y-%m-%d')}"

    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background: #f0f2f5; padding: 20px;">

        <div style="max-width: 600px; margin: auto; background: white;
                    border-radius: 12px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">

            <h2 style="color: #1a1a2e; border-bottom: 2px solid #06b6d4; padding-bottom: 10px;">
                🧠 KGB — Daily Intelligence Report
            </h2>

            <p style="color: #64748b;">
                <strong>Date:</strong> {datetime.datetime.utcnow().strftime('%B %d, %Y')}
            </p>

            <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                <tr style="background: #f8fafc;">
                    <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">
                        📋 Total Queries
                    </td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0; color: #3b82f6;">
                        {stats.get('total_queries', 0)}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">
                        ⏱️ Avg Response Time
                    </td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0; color: #34d399;">
                        {stats.get('avg_response_time', 0):.1f} ms
                    </td>
                </tr>
                <tr style="background: #f8fafc;">
                    <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">
                        🎯 Avg Similarity Score
                    </td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0; color: #a78bfa;">
                        {stats.get('avg_similarity', 0):.4f}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">
                        ⚡ Cache Hit Rate
                    </td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0; color: #f59e0b;">
                        {stats.get('cache_hit_rate', 0):.1f}%
                    </td>
                </tr>
                <tr style="background: #f8fafc;">
                    <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">
                        🔢 Total Tokens Used
                    </td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0; color: #f43f5e;">
                        {stats.get('total_tokens_used', 0):,}
                    </td>
                </tr>
                <tr>
                    <td style="padding: 12px; border: 1px solid #e2e8f0; font-weight: bold;">
                        🤖 Model
                    </td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">
                        Mistral 7B
                    </td>
                </tr>
            </table>

            <p style="color: #94a3b8; font-size: 12px; margin-top: 20px; text-align: center;">
                Powered by KGB Enterprise Intelligence Platform
            </p>
        </div>
    </body>
    </html>
    """

    # Create email message
    msg                    = MIMEMultipart('alternative')
    msg['Subject']         = subject
    msg['From']            = EMAIL_SENDER
    msg['To']              = EMAIL_RECEIVER
    msg.attach(MIMEText(body, 'html'))

    # Send via Gmail SMTP
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("✅ Email notification sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Email notification failed: {e}")
        return False


# ══════════════════════════════════════════════════
# SEND DAILY SUMMARY (Both Slack + Email)
# ══════════════════════════════════════════════════
def send_daily_summary(stats):
    """Sends daily summary to both Slack and Email"""
    print("📤 Sending daily summary notifications...")
    send_slack_summary(stats)
    send_email_summary(stats)
    print("✅ All notifications sent!")
