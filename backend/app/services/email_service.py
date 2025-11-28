from typing import Optional
from app.core.config import settings
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

class EmailService:
    def send_verification_email(self, email_to: str, token: str, username: str):
        """Send email verification link to user"""
        subject = f"{settings.PROJECT_NAME} - Verify your email"
        link = f"{settings.FRONTEND_URL}/verify-email/{token}"
        
        html_content = self._get_verification_email_template(username, link)
        text_content = f"""
        Hi {username},
        
        Welcome to {settings.PROJECT_NAME}!
        
        Please verify your email address by clicking the link below:
        {link}
        
        This link will expire in 24 hours.
        
        If you didn't create an account, please ignore this email.
        
        Best regards,
        The {settings.PROJECT_NAME} Team
        """
        
        self._send_email(email_to, subject, html_content, text_content)

    def send_password_reset_email(self, email_to: str, token: str, username: str):
        """Send password reset link to user"""
        subject = f"{settings.PROJECT_NAME} - Password Reset Request"
        link = f"{settings.FRONTEND_URL}/reset-password/{token}"
        
        html_content = self._get_password_reset_email_template(username, link)
        text_content = f"""
        Hi {username},
        
        We received a request to reset your password for your {settings.PROJECT_NAME} account.
        
        Click the link below to reset your password:
        {link}
        
        This link will expire in 1 hour.
        
        If you didn't request a password reset, please ignore this email or contact support if you have concerns.
        
        Best regards,
        The {settings.PROJECT_NAME} Team
        """
        
        self._send_email(email_to, subject, html_content, text_content)

    def _send_email(self, email_to: str, subject: str, html_content: str, text_content: str):
        """Send email via SMTP or log to console in development"""
        
        # Development mode: log to console (only if SMTP not configured)
        if not settings.SMTP_HOST or not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            logger.info("="*80)
            logger.info(f"📧 EMAIL TO: {email_to}")
            logger.info(f"📧 SUBJECT: {subject}")
            logger.info("="*80)
            logger.info(text_content)
            logger.info("="*80)
            print(f"\n{'='*80}\n📧 EMAIL TO: {email_to}\n📧 SUBJECT: {subject}\n{'='*80}\n{text_content}\n{'='*80}\n")
            logger.warning("SMTP credentials not configured. Email logged to console only.")
            return
        
        # Production mode: send via SMTP
        try:
            smtp_host = settings.SMTP_HOST
            smtp_port = settings.SMTP_PORT or 587
            smtp_timeout = getattr(settings, "SMTP_TIMEOUT", 15) or 15

            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = settings.EMAILS_FROM_EMAIL or settings.SMTP_USER
            msg['To'] = email_to
            
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            
            msg.attach(part1)
            msg.attach(part2)
            
            with smtplib.SMTP(smtp_host, smtp_port, timeout=smtp_timeout) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
                
            logger.info(f"✅ Email sent successfully to {email_to}")
            print(f"✅ Email sent successfully to {email_to}")
        except Exception as e:
            logger.error(f"❌ Failed to send email to {email_to}: {str(e)}")
            print(f"❌ Failed to send email to {email_to}: {str(e)}")
            # Fall back to console logging if SMTP fails
            print(f"\n{'='*80}\n📧 EMAIL TO: {email_to}\n📧 SUBJECT: {subject}\n{'='*80}\n{text_content}\n{'='*80}\n")

    def _get_verification_email_template(self, username: str, link: str) -> str:
        """HTML template for verification email"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verify Your Email</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <tr>
                                <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; text-align: center;">
                                    <h1 style="color: #ffffff; margin: 0; font-size: 28px;">Welcome to {settings.PROJECT_NAME}!</h1>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 40px;">
                                    <h2 style="color: #333333; margin-top: 0;">Hi {username},</h2>
                                    <p style="color: #666666; font-size: 16px; line-height: 1.6;">
                                        Thank you for creating an account with {settings.PROJECT_NAME}. 
                                        To get started, please verify your email address by clicking the button below.
                                    </p>
                                    <div style="text-align: center; margin: 30px 0;">
                                        <a href="{link}" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; padding: 14px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">
                                            Verify Email Address
                                        </a>
                                    </div>
                                    <p style="color: #666666; font-size: 14px; line-height: 1.6;">
                                        Or copy and paste this link into your browser:<br>
                                        <a href="{link}" style="color: #667eea; word-break: break-all;">{link}</a>
                                    </p>
                                    <p style="color: #999999; font-size: 12px; margin-top: 30px;">
                                        This link will expire in 24 hours. If you didn't create an account, please ignore this email.
                                    </p>
                                </td>
                            </tr>
                            <tr>
                                <td style="background-color: #f8f9fa; padding: 20px; text-align: center;">
                                    <p style="color: #999999; font-size: 12px; margin: 0;">
                                        © 2025 {settings.PROJECT_NAME}. All rights reserved.
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

    def _get_password_reset_email_template(self, username: str, link: str) -> str:
        """HTML template for password reset email"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reset Your Password</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <tr>
                                <td style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 40px; text-align: center;">
                                    <h1 style="color: #ffffff; margin: 0; font-size: 28px;">Password Reset Request</h1>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 40px;">
                                    <h2 style="color: #333333; margin-top: 0;">Hi {username},</h2>
                                    <p style="color: #666666; font-size: 16px; line-height: 1.6;">
                                        We received a request to reset your password for your {settings.PROJECT_NAME} account.
                                        Click the button below to create a new password.
                                    </p>
                                    <div style="text-align: center; margin: 30px 0;">
                                        <a href="{link}" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: #ffffff; padding: 14px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">
                                            Reset Password
                                        </a>
                                    </div>
                                    <p style="color: #666666; font-size: 14px; line-height: 1.6;">
                                        Or copy and paste this link into your browser:<br>
                                        <a href="{link}" style="color: #f5576c; word-break: break-all;">{link}</a>
                                    </p>
                                    <p style="color: #999999; font-size: 12px; margin-top: 30px;">
                                        This link will expire in 1 hour. If you didn't request a password reset, 
                                        please ignore this email or contact support if you have concerns.
                                    </p>
                                </td>
                            </tr>
                            <tr>
                                <td style="background-color: #f8f9fa; padding: 20px; text-align: center;">
                                    <p style="color: #999999; font-size: 12px; margin: 0;">
                                        © 2025 {settings.PROJECT_NAME}. All rights reserved.
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

    def send_claim_status_email(self, email_to: str, username: str, item_title: str, status: str, admin_notes: Optional[str] = None):
        """Send claim status update email to user"""
        subject = f"{settings.PROJECT_NAME} - Claim Update: {item_title}"
        
        html_content = self._get_claim_status_email_template(username, item_title, status, admin_notes)
        
        status_text = "approved" if status == "verified" else "rejected"
        
        text_content = f"""
        Hi {username},
        
        Your claim for the item "{item_title}" has been {status_text}.
        
        Status: {status.upper()}
        """
        
        if admin_notes:
            text_content += f"\nAdmin Notes: {admin_notes}\n"
            
        text_content += f"""
        You can view the details in your dashboard:
        {settings.FRONTEND_URL}/dashboard
        
        Best regards,
        The {settings.PROJECT_NAME} Team
        """
        
        self._send_email(email_to, subject, html_content, text_content)

    def _get_claim_status_email_template(self, username: str, item_title: str, status: str, admin_notes: Optional[str] = None) -> str:
        """HTML template for claim status email"""
        status_color = "#48bb78" if status == "verified" else "#f56565"
        status_text = "Approved" if status == "verified" else "Rejected"
        status_message = "Congratulations! Your claim has been verified." if status == "verified" else "We're sorry, but your claim has been rejected."
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Claim Status Update</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <tr>
                                <td style="background: linear-gradient(135deg, {status_color} 0%, #2d3748 100%); padding: 40px; text-align: center;">
                                    <h1 style="color: #ffffff; margin: 0; font-size: 28px;">Claim {status_text}</h1>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 40px;">
                                    <h2 style="color: #333333; margin-top: 0;">Hi {username},</h2>
                                    <p style="color: #666666; font-size: 16px; line-height: 1.6;">
                                        {status_message}
                                    </p>
                                    
                                    <div style="background-color: #f8f9fa; border-left: 4px solid {status_color}; padding: 15px; margin: 20px 0;">
                                        <p style="margin: 0; color: #4a5568; font-weight: bold;">Item: {item_title}</p>
                                        <p style="margin: 5px 0 0 0; color: #718096;">Status: <span style="color: {status_color}; font-weight: bold;">{status.upper()}</span></p>
                                        {f'<p style="margin: 10px 0 0 0; color: #4a5568;"><strong>Admin Notes:</strong><br>{admin_notes}</p>' if admin_notes else ''}
                                    </div>
                                    
                                    <div style="text-align: center; margin: 30px 0;">
                                        <a href="{settings.FRONTEND_URL}/dashboard" style="background-color: #4a5568; color: #ffffff; padding: 14px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">
                                            View Dashboard
                                        </a>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td style="background-color: #f8f9fa; padding: 20px; text-align: center;">
                                    <p style="color: #999999; font-size: 12px; margin: 0;">
                                        © 2025 {settings.PROJECT_NAME}. All rights reserved.
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

email_service = EmailService()
