import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { authService } from '../services/api';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Alert, AlertDescription } from '../components/ui/alert';
import { Loader2, CheckCircle2, XCircle, Mail } from 'lucide-react';

const VerifyEmail = () => {
    const { token } = useParams();
    const navigate = useNavigate();
    const [status, setStatus] = useState('verifying'); // verifying, success, error
    const [message, setMessage] = useState('');
    const [email, setEmail] = useState('');
    const [resending, setResending] = useState(false);

    useEffect(() => {
        const verifyEmailToken = async () => {
            if (!token) {
                setStatus('error');
                setMessage('Invalid verification link');
                return;
            }

            try {
                const data = await authService.verifyEmail(token);
                setStatus('success');
                setMessage(data.message || 'Email verified successfully!');

                // Redirect to login after 3 seconds
                setTimeout(() => {
                    navigate('/login');
                }, 3000);
            } catch (error) {
                setStatus('error');
                setMessage(error.response?.data?.detail || 'Verification failed. The link may be invalid or expired.');
            }
        };

        verifyEmailToken();
    }, [token, navigate]);

    const handleResendVerification = async () => {
        if (!email) {
            setMessage('Please enter your email address');
            return;
        }

        setResending(true);
        try {
            const data = await authService.resendVerification(email);
            setMessage(data.message || 'Verification email sent! Please check your inbox.');
            setStatus('success');
        } catch (error) {
            setMessage(error.response?.data?.detail || 'Failed to resend verification email');
        } finally {
            setResending(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md w-full">
                <div className="text-center mb-8">
                    <h2 className="text-3xl font-bold text-gray-900">Email Verification</h2>
                </div>

                <Card className="p-6">
                    <div className="text-center">
                        {status === 'verifying' && (
                            <>
                                <Loader2 className="w-16 h-16 mx-auto text-blue-600 animate-spin mb-4" />
                                <h3 className="text-xl font-semibold text-gray-900 mb-2">Verifying your email...</h3>
                                <p className="text-gray-600">Please wait while we verify your email address.</p>
                            </>
                        )}

                        {status === 'success' && (
                            <>
                                <CheckCircle2 className="w-16 h-16 mx-auto text-green-600 mb-4" />
                                <h3 className="text-xl font-semibold text-gray-900 mb-2">Email Verified!</h3>
                                <Alert className="mt-4 mb-4">
                                    <AlertDescription>{message}</AlertDescription>
                                </Alert>
                                <p className="text-gray-600 mb-4">Redirecting to login page...</p>
                                <Button onClick={() => navigate('/login')} className="w-full">
                                    Go to Login
                                </Button>
                            </>
                        )}

                        {status === 'error' && (
                            <>
                                <XCircle className="w-16 h-16 mx-auto text-red-600 mb-4" />
                                <h3 className="text-xl font-semibold text-gray-900 mb-2">Verification Failed</h3>
                                <Alert variant="destructive" className="mt-4 mb-4">
                                    <AlertDescription>{message}</AlertDescription>
                                </Alert>

                                <div className="mt-6 space-y-4">
                                    <p className="text-sm text-gray-600">Need a new verification link?</p>
                                    <div className="relative">
                                        <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                                        <input
                                            type="email"
                                            placeholder="Enter your email"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                        />
                                    </div>
                                    <Button
                                        onClick={handleResendVerification}
                                        disabled={resending}
                                        className="w-full"
                                    >
                                        {resending ? (
                                            <>
                                                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                                Sending...
                                            </>
                                        ) : (
                                            'Resend Verification Email'
                                        )}
                                    </Button>

                                    <Link to="/login" className="block text-center text-sm text-blue-600 hover:text-blue-500">
                                        Back to Login
                                    </Link>
                                </div>
                            </>
                        )}
                    </div>
                </Card>
            </div>
        </div>
    );
};

export default VerifyEmail;
