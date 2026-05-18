#!/usr/bin/env python3
"""
Send an HTML email via Gmail SMTP.

Required env vars:
  GMAIL_USER          sender/recipient address (e.g. you@gmail.com)
  GMAIL_APP_PASSWORD  Gmail App Password (Account Google → Sicurezza → Password per le app)

Usage:
  python3 gmail_send.py --subject "..." --html "<html>...</html>"
  python3 gmail_send.py --subject "..." --html-file body.html
"""

import argparse
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send(subject: str, html_body: str, sender: str, app_password: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = sender
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.sendmail(sender, sender, msg.as_string())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--html", help="HTML body as string")
    group.add_argument("--html-file", help="Path to file containing HTML body")
    args = parser.parse_args()

    sender = os.environ.get("GMAIL_USER")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")

    if not sender or not app_password:
        print(
            "ERROR: Set GMAIL_USER and GMAIL_APP_PASSWORD environment variables.",
            file=sys.stderr,
        )
        sys.exit(1)

    html_body = args.html
    if args.html_file:
        with open(args.html_file) as f:
            html_body = f.read()

    send(args.subject, html_body, sender, app_password)
    print(f"Email sent: {args.subject}")


if __name__ == "__main__":
    main()
