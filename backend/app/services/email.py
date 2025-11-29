import logging
from typing import List

import requests

from app.core.config import settings

logger = logging.getLogger(__name__)

RESEND_API_URL = "https://api.resend.com/emails"


def _ensure_config():
    if not settings.RESEND_API_KEY:
        raise RuntimeError("RESEND_API_KEY is not configured.")
    if not settings.RESEND_FROM_EMAIL:
        raise RuntimeError("RESEND_FROM_EMAIL is not configured.")
    if not settings.FRONTEND_URL:
        raise RuntimeError("FRONTEND_URL is not configured.")


def send_resend_email(to_emails: List[str], subject: str, html_content: str):
    """
    Low-level helper that sends an email through Resend's HTTP API.
    Raises RuntimeError when the API returns a non-successful response.
    """
    _ensure_config()

    headers = {
        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "from": settings.RESEND_FROM_EMAIL,
        "to": to_emails,
        "subject": subject,
        "html": html_content,
    }

    logger.info(f"📧 Sending Resend email to {to_emails} with subject '{subject}'")
    response = requests.post(RESEND_API_URL, json=payload, headers=headers, timeout=15)

    if response.status_code >= 400:
        logger.error(
            "❌ Resend email failed | status=%s | body=%s",
            response.status_code,
            response.text,
        )
        raise RuntimeError(
            f"Resend email failed with status {response.status_code}: {response.text}"
        )

    logger.info("✅ Resend email sent successfully to %s", to_emails)
    return response.json()


def send_verification_email(to_email: str, token: str):
    """
    Send a verification email with a Resend-powered button that points to the frontend.
    """
    verification_url = f"{settings.FRONTEND_URL.rstrip('/')}/verify-email?token={token}"
    subject = f"{settings.PROJECT_NAME} - Verify your email"
    html = f"""
    <div style="font-family: Arial, sans-serif; color: #1f2933; background-color:#f5f7fa; padding:32px;">
        <div style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:12px;box-shadow:0 10px 35px rgba(15,23,42,0.08);overflow:hidden;">
            <div style="padding:32px;border-bottom:1px solid #e5e7eb;">
                <h1 style="margin:0;font-size:20px;color:#111827;">Confirm your email</h1>
                <p style="margin:12px 0 0;font-size:15px;line-height:1.6;color:#4b5563;">
                    Thanks for registering with {settings.PROJECT_NAME}. To keep things secure we need to
                    confirm this email address before you can sign in.
                </p>
            </div>
            <div style="padding:32px;text-align:center;">
                <a href="{verification_url}"
                   style="display:inline-block;background:linear-gradient(135deg,#2563eb,#7c3aed);color:#ffffff;
                          padding:14px 28px;border-radius:999px;font-weight:bold;text-decoration:none;font-size:16px;">
                    Verify email
                </a>
                <p style="margin:24px 0 0;font-size:13px;color:#6b7280;">
                    This link expires in 24 hours. If the button does not work, copy and paste this URL into your browser:
                </p>
                <p style="margin:12px 0 0;font-size:13px;word-break:break-all;color:#2563eb;">
                    {verification_url}
                </p>
            </div>
            <div style="background:#f9fafb;padding:20px;text-align:center;font-size:12px;color:#9ca3af;">
                © {settings.PROJECT_NAME}. All rights reserved.
            </div>
        </div>
    </div>
    """
    send_resend_email([to_email], subject, html)


def send_password_reset_email(to_email: str, token: str):
    reset_url = f"{settings.FRONTEND_URL.rstrip('/')}/reset-password/{token}"
    subject = f"{settings.PROJECT_NAME} - Reset your password"
    html = f"""
    <div style="font-family: Arial, sans-serif; color: #1f2933; background-color:#fef2f2; padding:32px;">
        <div style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:12px;box-shadow:0 10px 35px rgba(15,23,42,0.08);overflow:hidden;">
            <div style="padding:32px;border-bottom:1px solid #fee2e2;">
                <h1 style="margin:0;font-size:20px;color:#b91c1c;">Reset password</h1>
                <p style="margin:12px 0 0;font-size:15px;line-height:1.6;color:#4b5563;">
                    Someone requested a password reset for your {settings.PROJECT_NAME} account. If this was you,
                    click the button below to pick a new password.
                </p>
            </div>
            <div style="padding:32px;text-align:center;">
                <a href="{reset_url}"
                   style="display:inline-block;background:#dc2626;color:#ffffff;
                          padding:14px 28px;border-radius:999px;font-weight:bold;text-decoration:none;font-size:16px;">
                    Reset password
                </a>
                <p style="margin:24px 0 0;font-size:13px;color:#6b7280;">
                    This link expires in 60 minutes. If you didn't request this change you can safely ignore the email.
                </p>
                <p style="margin:12px 0 0;font-size:13px;word-break:break-all;color:#dc2626;">
                    {reset_url}
                </p>
            </div>
            <div style="background:#f9fafb;padding:20px;text-align:center;font-size:12px;color:#9ca3af;">
                © {settings.PROJECT_NAME}. All rights reserved.
            </div>
        </div>
    </div>
    """
    send_resend_email([to_email], subject, html)


def send_claim_status_email(
    to_email: str,
    username: str,
    item_title: str,
    status: str,
    admin_notes: str | None = None,
):
    status_map = {
        "verified": ("#10b981", "Approved", "Congrats! Your claim has been approved."),
        "rejected": ("#ef4444", "Rejected", "Unfortunately your claim was rejected."),
    }
    color, title, message = status_map.get(
        status,
        ("#3b82f6", status.title(), "Your claim has been updated."),
    )

    subject = f"{settings.PROJECT_NAME} - Claim update"
    notes_html = (
        f"<p style='margin:16px 0 0;font-size:14px;color:#111827;'>"
        f"<strong>Admin notes:</strong><br>{admin_notes}</p>"
        if admin_notes
        else ""
    )
    html = f"""
    <div style="font-family: Arial, sans-serif; color: #111827; background-color:#f4f5f7; padding:32px;">
        <div style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:12px;box-shadow:0 10px 35px rgba(15,23,42,0.08);overflow:hidden;">
            <div style="padding:32px;border-bottom:1px solid #e5e7eb;">
                <h1 style="margin:0;font-size:20px;color:{color};">{title}</h1>
                <p style="margin:12px 0 0;font-size:15px;line-height:1.6;color:#4b5563;">
                    Hi {username}, {message}
                </p>
            </div>
            <div style="padding:32px;">
                <p style="margin:0;font-size:15px;color:#111827;">
                    Item: <strong>{item_title}</strong>
                </p>
                <p style="margin:8px 0 0;font-size:14px;color:#6b7280;">
                    Status: <span style="color:{color};font-weight:bold;">{status.upper()}</span>
                </p>
                {notes_html}
            </div>
            <div style="padding:0 32px 32px;text-align:center;">
                <a href="{settings.FRONTEND_URL.rstrip('/')}/dashboard"
                   style="display:inline-block;background:#111827;color:#ffffff;
                          padding:14px 28px;border-radius:999px;font-weight:bold;text-decoration:none;font-size:16px;">
                    View dashboard
                </a>
            </div>
            <div style="background:#f9fafb;padding:20px;text-align:center;font-size:12px;color:#9ca3af;">
                © {settings.PROJECT_NAME}. All rights reserved.
            </div>
        </div>
    </div>
    """
    send_resend_email([to_email], subject, html)

