from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import random

def generate_otp():
    return str(random.randint(100000, 999999))

def send_reset_email(user, reset_url, otp):
    subject = " Password Reset for Cyman Wear"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    text_content = f"""Hi {user.username},

You requested a password reset for your Cyman Wear account.

Reset Link: {reset_url}
OTP Code: {otp}

This link and OTP will expire in 15 minutes. If you didn’t request this, you can safely ignore this email.
"""

    html_content = f"""
    <div style="font-family:Arial, sans-serif; background:#f9f9f9; padding:20px;">
        <h2 style="color:#333;">Reset Your Cyman Wear Password</h2>
        <p>Hello <strong>{user.username}</strong>,</p>
        <p>We received a request to reset your password.</p>
        <p>
            <a href="{reset_url}" style="background:#000; color:#fff; padding:10px 15px; text-decoration:none; border-radius:4px;">
                Reset Password
            </a>
        </p>
        <p>Your One-Time Password (OTP): <strong>{otp}</strong></p>
        <p style="margin-top:10px;">This link and OTP expire in 15 minutes.</p>
        <hr style="margin-top:30px;">
        <small style="color:#888;">Cyman Wear — Where Confidence Meets Comfort.</small>
    </div>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
    except Exception as e:
        print(f" Email delivery failed: {e}")