# Email Sending Debugging Guide

## Issues Fixed

### 1. Background Task Closure Issue
**Problem**: The background task was capturing the `user` object directly, which could cause issues if the database session closes before the task executes.

**Fix**: Now capturing the values (`user_email`, `user_token`, `user_username`) before creating the background task to avoid closure issues.

### 2. Insufficient Logging
**Problem**: Not enough logging to track email sending progress.

**Fix**: Added detailed logging at every step:
- When email task is queued
- When background task starts
- When email service is called
- Each step of SMTP connection (connect, TLS, auth, send)
- Success/failure messages

### 3. No Way to Test Email Sending
**Problem**: No easy way to verify if email sending works.

**Fix**: Added `/api/v1/auth/test-email` endpoint that:
- Shows SMTP configuration status
- Attempts to send a test email
- Returns detailed error messages if it fails

## How to Debug Email Issues

### Step 1: Check Backend Logs on Render

After deployment, check the Render logs for:

#### Startup Logs (should appear when backend starts):
```
🚀 Starting Lost & Found API
✅ SMTP configured: smtp.gmail.com:587
   From: priyeshsingh1101@gmail.com
   Email sending is ENABLED
```

OR if not configured:
```
⚠️  SMTP NOT FULLY CONFIGURED:
   SMTP_HOST: ❌
   SMTP_USER: ❌
   SMTP_PASSWORD: ❌
   ⚠️  Emails will be logged to console only!
```

#### Registration Logs (when user registers):
```
📧 Verification email task queued for user@example.com (token: ABC123...)
📧 Background task started: Sending verification email to user@example.com
📧 send_verification_email called for user@example.com
📧 Verification link: https://lost-found-pri.vercel.app/verify-email/ABC123...
📧 Calling _send_email for user@example.com
📧 Attempting to send email to user@example.com via smtp.gmail.com:587
🔌 Connecting to SMTP server smtp.gmail.com:587...
🔐 Starting TLS...
🔑 Authenticating as priyeshsingh1101@gmail.com...
📤 Sending email to user@example.com...
✅ Email sent successfully to user@example.com
✅ Verification email sent successfully to user@example.com
```

### Step 2: Use Test Email Endpoint

1. **Login to your account** (or create one and verify it manually in database)
2. **Call the test endpoint**:
   ```bash
   POST https://priyesh-lost-n-found-backend.onrender.com/api/v1/auth/test-email
   Authorization: Bearer YOUR_TOKEN
   ```

3. **Check the response**:
   ```json
   {
     "status": "success",
     "message": "Test email sent to your@email.com. Check your inbox!",
     "smtp_config": {
       "SMTP_HOST": "smtp.gmail.com",
       "SMTP_PORT": 587,
       "SMTP_USER": "priyeshsingh1101@gmail.com",
       "SMTP_PASSWORD": "SET",
       "FRONTEND_URL": "https://lost-found-pri.vercel.app"
     }
   }
   ```

   OR if there's an error:
   ```json
   {
     "status": "error",
     "message": "SMTP Authentication failed...",
     "smtp_config": {...},
     "error_type": "SMTPAuthenticationError"
   }
   ```

### Step 3: Common Issues and Solutions

#### Issue: "SMTP NOT FULLY CONFIGURED" in startup logs
**Solution**: 
- Go to Render dashboard → Your backend service → Environment
- Add/update these environment variables:
  - `SMTP_HOST=smtp.gmail.com`
  - `SMTP_PORT=587`
  - `SMTP_USER=priyeshsingh1101@gmail.com`
  - `SMTP_PASSWORD=your_app_password` (⚠️ Use Gmail App Password, not regular password)
- Redeploy the backend

#### Issue: "SMTP Authentication failed"
**Solution**:
- **Use Gmail App Password**, not your regular Gmail password
- To get App Password:
  1. Go to Google Account → Security
  2. Enable 2-Step Verification (required)
  3. Go to "App passwords"
  4. Generate new password for "Mail"
  5. Use the 16-character password as `SMTP_PASSWORD`
- Update `SMTP_PASSWORD` in Render environment variables
- Redeploy

#### Issue: "Failed to connect to SMTP server"
**Solution**:
- Check `SMTP_HOST` is correct: `smtp.gmail.com`
- Check `SMTP_PORT` is correct: `587` (for TLS) or `465` (for SSL)
- Check firewall/network allows outbound SMTP connections
- Some hosting providers block SMTP ports - check Render's network policies

#### Issue: Emails sent but not received
**Solution**:
- Check spam/junk folder
- Verify email address is correct
- Check Gmail account for security alerts
- Verify `FRONTEND_URL` is correct in environment variables
- Wait a few minutes - email delivery can be delayed

#### Issue: No logs appear when registering
**Possible causes**:
- Background task not executing (check Render logs for errors)
- Database session closed before task runs (should be fixed now)
- Email service not being called (check logs for "📧 send_verification_email called")

### Step 4: Manual Database Verification

If emails aren't being sent, verify the user was created:

1. Check Railway database - user should exist with:
   - `is_verified = 0`
   - `verification_token` should have a value
   - `created_at` should be recent

2. If user exists but no email sent:
   - Check Render logs for email sending errors
   - Use test-email endpoint to verify SMTP works
   - Check if background tasks are executing

## Expected Behavior

### Successful Email Sending:
1. User registers → API responds in < 2 seconds
2. Background task queues email
3. Email is sent via SMTP
4. User receives verification email
5. User clicks link → email verified
6. User can login

### Log Flow:
```
[INFO] 📧 Verification email task queued for user@example.com
[INFO] 📧 Background task started: Sending verification email to user@example.com
[INFO] 📧 send_verification_email called for user@example.com
[INFO] 📧 Attempting to send email to user@example.com via smtp.gmail.com:587
[INFO] 🔌 Connecting to SMTP server smtp.gmail.com:587...
[INFO] 🔐 Starting TLS...
[INFO] 🔑 Authenticating as priyeshsingh1101@gmail.com...
[INFO] 📤 Sending email to user@example.com...
[INFO] ✅ Email sent successfully to user@example.com
```

## Next Steps

1. **Check Render logs** after deployment for SMTP configuration status
2. **Test registration** and watch logs for email sending progress
3. **Use test-email endpoint** if emails aren't being sent
4. **Verify SMTP credentials** are correct (especially App Password for Gmail)
5. **Check spam folder** if email sent but not received

## Files Modified

1. **`backend/app/api/v1/endpoints/auth.py`**
   - Fixed background task closure issue
   - Added detailed logging
   - Added test-email endpoint

2. **`backend/app/services/email_service.py`**
   - Added detailed logging at each step
   - Better error messages

