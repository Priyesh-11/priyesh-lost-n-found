import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { claimsService } from '../services/api';
import { Loader2, ShieldCheck, Clock, CheckCircle, XCircle } from 'lucide-react';
import { format } from 'date-fns';

const MyClaims = () => {
    const navigate = useNavigate();
    const [claims, setClaims] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchClaims = async () => {
            try {
                const data = await claimsService.getMyClaims();
                setClaims(data);
            } catch (error) {
                console.error("Failed to fetch claims:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchClaims();
    }, []);

    const getStatusBadge = (status) => {
        switch (status) {
            case 'verified':
                return <Badge className="bg-green-100 text-green-700 border-green-200">Verified</Badge>;
            case 'rejected':
                return <Badge className="bg-red-100 text-red-700 border-red-200">Rejected</Badge>;
            default:
                return <Badge className="bg-yellow-100 text-yellow-700 border-yellow-200">Pending</Badge>;
        }
    };

    const getStatusIcon = (status) => {
        switch (status) {
            case 'verified':
                return <CheckCircle className="w-5 h-5 text-green-600" />;
            case 'rejected':
                return <XCircle className="w-5 h-5 text-red-600" />;
            default:
                return <Clock className="w-5 h-5 text-yellow-600" />;
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">My Claims</h1>
                    <p className="text-gray-600">Track the status of your item claims</p>
                </div>

                {claims.length > 0 ? (
                    <div className="space-y-3 sm:space-y-4">\n                        {claims.map((claim) => (
                        <Card key={claim.id} className="p-4 sm:p-5 md:p-6 hover:shadow-md transition-shadow">
                            <div className="flex flex-col gap-3 sm:gap-4">
                                {/* Header */}
                                <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 sm:gap-4">
                                    <div className="flex-1">
                                        <div className="flex items-start gap-2 mb-1.5">
                                            <h3 className="text-base sm:text-lg font-semibold text-gray-900 flex-1">
                                                {claim.item_title || `Item #${claim.item_id}`}
                                            </h3>
                                            {getStatusBadge(claim.status)}
                                        </div>

                                        {/* Item metadata */}
                                        <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs sm:text-sm text-gray-600">
                                            {claim.item_type && (
                                                <span className="inline-flex items-center px-2 py-0.5 rounded bg-gray-100 text-gray-700 font-medium">
                                                    {claim.item_type === 'lost' ? '🔍 Lost' : '✅ Found'}
                                                </span>
                                            )}
                                            {claim.item_category && (
                                                <span className="inline-flex items-center px-2 py-0.5 rounded bg-blue-50 text-blue-700">
                                                    {claim.item_category}
                                                </span>
                                            )}
                                            <span className="text-gray-500">
                                                • Claim ID: #{claim.id}
                                            </span>
                                        </div>
                                    </div>

                                    <div className="flex sm:flex-col items-center sm:items-end gap-3 sm:gap-2">
                                        {getStatusIcon(claim.status)}
                                        <Button
                                            variant="outline"
                                            size="sm"
                                            onClick={() => navigate(`/items/${claim.item_id}`)}
                                            className="text-xs sm:text-sm"
                                        >
                                            View Item
                                        </Button>
                                    </div>
                                </div>

                                {/* Claim details */}
                                <div className="space-y-2 text-sm text-gray-600 border-t pt-3">
                                    <div>
                                        <span className="font-medium text-gray-900">Submitted:</span>
                                        <span className="ml-2">{format(new Date(claim.created_at), 'MMM dd, yyyy')}</span>
                                    </div>
                                    <div>
                                        <span className="font-medium text-gray-900">Proof Description:</span>
                                        <p className="mt-1 text-gray-700">{claim.proof_description}</p>
                                    </div>

                                    {claim.admin_notes && (
                                        <div className="bg-gray-50 p-3 rounded-md mt-2 border border-gray-200">\n                                                <p className="font-medium text-gray-900 text-sm mb-1">Admin Response:</p>
                                            <p className="text-gray-700 text-sm">{claim.admin_notes}</p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </Card>
                    ))}
                    </div>
                ) : (
                    <div className="text-center py-12 bg-white rounded-lg shadow-sm border border-gray-200">
                        <ShieldCheck className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">No Claims Yet</h3>
                        <p className="text-gray-600 mb-4">You haven't claimed any found items yet.</p>
                        <Button onClick={() => navigate('/items')}>Browse Found Items</Button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default MyClaims;
