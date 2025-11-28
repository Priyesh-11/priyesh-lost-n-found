import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { authService } from '../services/api';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card } from '../components/ui/card';
import { Alert, AlertDescription } from '../components/ui/alert';
import { Loader2, Mail, CheckCircle2 } from 'lucide-react';

const ForgotPassword = () => {
    const location = useLocation();
    const isResendVerification = location.state?.resendVerification || false;
    const [email, setEmail] = useState(location.state?.email || '');
    const [loading, setLoading] = useState(false);
    const [submitted, setSubmitted] = useState(false);
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');
    
    useEffect(() => {
        if (location.state?.email) {
            setEmail(location.state.email);
        }
    }, [location.state]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setMessage('');

        if (!email) {
            setError('Please enter your email address');
            return;
        }

        if (!/\S+@\S+\.\S+/.test(email)) {
            setError('Please enter a valid email address');
            return;
        }

        setLoading(true);
        try {
            let data;
            if (isResendVerification) {
                data = await authService.resendVerification(email);
                setMessage(data.message || 'Verification email has been resent! Please check your inbox.');
            } else {
                data = await authService.forgotPassword(email);
                setMessage(data.message || 'Password reset instructions have been sent to your email.');
            }
            setSubmitted(true);
        } catch (error) {
            const defaultMsg = isResendVerification 
                ? 'If your email is registered, you will receive a verification email.'
                : 'If your email is registered, you will receive a password reset link.';
            setMessage(error.response?.data?.detail || defaultMsg);
            setSubmitted(true);
        } finally {
            setLoading(false);
        }
    };

    if (submitted) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
                <div className="max-w-md w-full">
                    <div className="text-center mb-8">
                        <h2 className="text-3xl font-bold text-gray-900">Check Your Email</h2>
                    </div>

                    <Card className="p-6">
                        <div className="text-center">
                            <CheckCircle2 className="w-16 h-16 mx-auto text-green-600 mb-4" />
                            <h3 className="text-xl font-semibold text-gray-900 mb-4">Email Sent!</h3>
                            <Alert className="mb-6">
                                <AlertDescription>{message}</AlertDescription>
                            </Alert>
                            <p className="text-gray-600 mb-6">
                                If you don't see the email, please check your spam folder.
                            </p>
                            <Link to="/login">
                                <Button className="w-full">Back to Login</Button>
                            </Link>
                        </div>
                    </Card>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md w-full">
                <div className="text-center mb-8">
                    <h2 className="text-3xl font-bold text-gray-900">
                        {isResendVerification ? 'Resend Verification Email' : 'Forgot Password'}
                    </h2>
                    <p className="mt-2 text-gray-600">
                        {isResendVerification
                            ? "Enter your email address and we'll send you a new verification email."
                            : "Enter your email address and we'll send you a link to reset your password."}
                    </p>
                </div>

                <Card className="p-6">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        {error && (
                            <Alert variant="destructive">
                                <AlertDescription>{error}</AlertDescription>
                            </Alert>
                        )}

                        <div className="space-y-2">
                            <Label htmlFor="email">Email Address</Label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                                <Input
                                    id="email"
                                    name="email"
                                    type="email"
                                    placeholder="john.doe@example.com"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="pl-10"
                                    autoFocus
                                />
                            </div>
                        </div>

                        <Button
                            type="submit"
                            className="w-full"
                            disabled={loading}
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                    Sending...
                                </>
                            ) : (
                                isResendVerification ? 'Resend Verification Email' : 'Send Reset Link'
                            )}
                        </Button>

                        <div className="text-center">
                            <Link
                                to="/login"
                                className="text-sm text-blue-600 hover:text-blue-500"
                            >
                                Back to Login
                            </Link>
                        </div>
                    </form>
                </Card>
            </div>
        </div>
    );
};

export default ForgotPassword;
