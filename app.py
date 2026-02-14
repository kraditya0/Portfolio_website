import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import (
    init_db, get_all_projects, get_all_services,
    get_all_skills, get_approved_testimonials
)
from seed_db import seed

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production-aditya-2026'

# ─── Email Configuration ───────────────────────────────────
# To use Gmail SMTP, generate an App Password:
# 1. Go to https://myaccount.google.com/apppasswords
# 2. Create an app password for "Mail"
# 3. Paste it below (16-char code, no spaces)
EMAIL_ADDRESS = 'aditya2003iitm@gmail.com'
EMAIL_APP_PASSWORD = os.environ.get('EMAIL_APP_PASSWORD', 'glekpgyaghqhjirt')

# ─── Initialize & seed DB on startup ───────────────────────
# On Vercel, /tmp is ephemeral so DB must be recreated each cold start

with app.app_context():
    try:
        init_db()
        seed()
    except Exception as e:
        print(f"[DB INIT ERROR] {e}")


# ─── Email Helper ───────────────────────────────────────────

def send_email(subject, body_html):
    """Send an email notification to the site owner."""
    if not EMAIL_APP_PASSWORD:
        print(f"[EMAIL NOT SENT - No app password configured] {subject}")
        print(body_html)
        return False

    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = subject
        msg.attach(MIMEText(body_html, 'html'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False


# ═══════════════════════════════════════════════════════════
#  PUBLIC ROUTES
# ═══════════════════════════════════════════════════════════

@app.route('/')
def index():
    projects = get_all_projects()
    services = get_all_services()
    skills = get_all_skills()
    testimonials = get_approved_testimonials()
    return render_template('index.html', projects=projects, services=services, skills=skills, testimonials=testimonials)


@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not email or not message:
        flash('All fields are required!', 'danger')
        return redirect(url_for('index') + '#contact')

    # Send email notification
    subject = f'Portfolio Contact: {name}'
    body = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;padding:20px;
                background:#0d1b2a;color:#e0e0e0;border-radius:10px;">
        <h2 style="color:#0d6efd;border-bottom:1px solid #1a3a5c;padding-bottom:10px;">
            New Contact Message
        </h2>
        <p><strong style="color:#6ea8fe;">Name:</strong> {name}</p>
        <p><strong style="color:#6ea8fe;">Email:</strong> <a href="mailto:{email}" style="color:#0d6efd;">{email}</a></p>
        <p><strong style="color:#6ea8fe;">Message:</strong></p>
        <div style="background:#112240;padding:15px;border-radius:8px;margin-top:5px;">
            {message}
        </div>
        <hr style="border-color:#1a3a5c;margin-top:20px;">
        <p style="color:#888;font-size:12px;">Sent from your portfolio website</p>
    </div>
    """
    send_email(subject, body)

    flash('Message sent successfully! I\'ll get back to you soon.', 'success')
    return redirect(url_for('index') + '#contact')


# ─── API endpoints for Vue.js ────────────────────────────────

@app.route('/api/projects')
def api_projects():
    projects = get_all_projects()
    return jsonify([dict(p) for p in projects])


@app.route('/api/services')
def api_services():
    services = get_all_services()
    return jsonify([dict(s) for s in services])


@app.route('/api/skills')
def api_skills():
    skills = get_all_skills()
    return jsonify([dict(s) for s in skills])


# ═══════════════════════════════════════════════════════════
#  RUN
# ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    app.run(debug=True, port=5000)
