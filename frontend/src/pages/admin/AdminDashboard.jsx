import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { claimsService, itemsService } from '../../services/api';
import { Button } from '../../components/ui/button';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { useToast } from '../../hooks/use-toast';
import { Loader2, CheckCircle, XCircle, AlertCircle, Package, Shield, History, Eye } from 'lucide-react';
import { format } from 'date-fns';

const AdminDashboard = () => {
    const { user, isAuthenticated } = useAuth();
    const navigate = useNavigate();
    const { toast } = useToast();
    const [activeTab, setActiveTab] = useState('claims');
    const [allClaims, setAllClaims] = useState([]);
    const [allItems, setAllItems] = useState([]);
    const [loading, setLoading] = useState(true);

    // Derived state for tabs
    const pendingClaims = allClaims.filter(c => c.status === 'pending');
    const historyClaims = allClaims
        .filter(c => c.status === 'verified' || c.status === 'rejected')
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at)); // Sort by newest first
    useEffect(() => {
        if (!isAuthenticated) {
            navigate('/login');
        } else if (user && user.role_id !== 2) {
            navigate('/');
            toast({
                title: "Access Denied",
                description: "You do not have permission to view this page.",
                variant: "destructive"
            });
        }
    }, [isAuthenticated, user, navigate, toast]);

    const fetchData = async () => {
        setLoading(true);
        try {
            // Fetch all data in parallel for stats
            const [claimsData, itemsData] = await Promise.all([
                claimsService.getAll(),
                itemsService.getAll({ status: 'all', limit: 100 })
            ]);

            setAllClaims(claimsData);

            const itemsList = Array.isArray(itemsData) ? itemsData : itemsData.items || [];
            setAllItems(itemsList);
        } catch (error) {
            console.error("Failed to fetch admin data:", error);
            toast({
                title: "Error",
                description: "Failed to load dashboard data",
                variant: "destructive"
            });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (user && user.role_id === 2) {
            fetchData();
        }
    }, [user]);

    const handleVerifyClaim = async (claimId, status) => {
        try {
            await claimsService.verify(claimId, { status });
            toast({
                title: status === 'verified' ? "Claim Verified" : "Claim Rejected",
                description: `Claim has been ${status}.`,
            });
            fetchData();
        } catch (error) {
            toast({
                title: "Error",
                description: "Failed to update claim status",
                variant: "destructive"
            });
        }
    };

    const handleResolveItem = async (itemId) => {
        try {
            await itemsService.resolve(itemId);
            toast({
                title: "Item Resolved",
                description: "Item marked as returned. Reputation points awarded.",
            });
            // Refresh data to remove claim from active list
            fetchData();
        } catch (error) {
            toast({
                title: "Error",
                description: "Failed to resolve item",
                variant: "destructive"
            });
        }
    };

    if (loading && !allClaims.length && !allItems.length) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-gray-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">

                {/* Header Section - Enhanced */}
                <div className="mb-6 sm:mb-8">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 sm:gap-0 mb-4">
                        <div>
                            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-1">Admin Dashboard</h1>
                            <p className="text-sm sm:text-base text-gray-600">Manage claims, items, and users</p>
                        </div>
                        <div className="flex items-center gap-2 bg-gradient-to-r from-purple-600 to-purple-500 text-white rounded-xl px-4 py-2 shadow-lg self-start sm:self-auto">
                            <Shield className="w-4 h-4 sm:w-5 sm:h-5" />
                            <span className="font-semibold text-sm sm:text-base">Admin Access</span>
                        </div>
                    </div>

                    {/* Stats Cards */}
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
                        <StatCard label="Pending Claims" value={allClaims.filter(c => c.status === 'pending').length} color="yellow" />
                        <StatCard label="Verified" value={allClaims.filter(c => c.status === 'verified').length} color="green" />
                        <StatCard label="Rejected" value={allClaims.filter(c => c.status === 'rejected').length} color="red" />
                        <StatCard label="Total Items" value={allItems.length} color="blue" />
                    </div>
                </div>

                <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
                    <TabsList className="bg-white p-1 border border-gray-200 rounded-xl shadow-sm inline-flex w-auto">
                        <TabsTrigger value="claims" className="px-4 sm:px-6 text-xs sm:text-sm whitespace-nowrap rounded-lg">
                            <AlertCircle className="w-4 h-4 mr-2" />
                            Claims Management
                        </TabsTrigger>
                        <TabsTrigger value="history" className="px-4 sm:px-6 text-xs sm:text-sm whitespace-nowrap rounded-lg">
                            <History className="w-4 h-4 mr-2" />
                            History
                        </TabsTrigger>
                        <TabsTrigger value="items" className="px-4 sm:px-6 text-xs sm:text-sm whitespace-nowrap rounded-lg">
                            <Package className="w-4 h-4 mr-2" />
                            Items
                        </TabsTrigger>
                    </TabsList>

                    {/* Claims Management Tab */}
                    <TabsContent value="claims">
                        <div className="grid gap-4">
                            {pendingClaims.length === 0 ? (
                                <Card className="p-8 text-center">
                                    <AlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                                    <p className="text-gray-600 font-medium">No pending claims</p>
                                    <p className="text-sm text-gray-500 mt-1">All claims have been processed</p>
                                </Card>
                            ) : (
                                pendingClaims.map((claim) => (
                                    <ClaimCard
                                        key={claim.id}
                                        claim={claim}
                                        onVerify={handleVerifyClaim}
                                        onResolve={handleResolveItem}
                                    />
                                ))
                            )}
                        </div>
                    </TabsContent>

                    {/* History Tab */}
                    <TabsContent value="history">
                        <div className="grid gap-4">
                            {historyClaims.length === 0 ? (
                                <Card className="p-8 text-center">
                                    <History className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                                    <p className="text-gray-600 font-medium">No claim history</p>
                                    <p className="text-sm text-gray-500 mt-1">Processed claims will appear here</p>
                                </Card>
                            ) : (
                                historyClaims.map((claim) => (
                                    <HistoryClaimCard key={claim.id} claim={claim} />
                                ))
                            )}
                        </div>
                    </TabsContent>

                    {/* Items Overview Tab */}
                    <TabsContent value="items">
                        <div className="grid gap-4">
                            {allItems.length === 0 ? (
                                <Card className="p-8 text-center">
                                    <Package className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                                    <p className="text-gray-600 font-medium">No items found</p>
                                </Card>
                            ) : (
                                allItems.map((item) => (
                                    <ItemCard
                                        key={item.id}
                                        item={item}
                                        onResolve={handleResolveItem}
                                    />
                                ))
                            )}
                        </div>
                    </TabsContent>
                </Tabs>
            </div>
        </div>
    );
};

// Stat Card Component
const StatCard = ({ label, value, color }) => {
    const colors = {
        yellow: 'bg-yellow-50 border-yellow-200 text-yellow-700',
        green: 'bg-green-50 border-green-200 text-green-700',
        red: 'bg-red-50 border-red-200 text-red-700',
        blue: 'bg-blue-50 border-blue-200 text-blue-700'
    };

    return (
        <div className={`${colors[color]} border rounded-xl p-3 sm:p-4`}>
            <div className="text-2xl sm:text-3xl font-bold mb-0.5">{value}</div>
            <div className="text-xs sm:text-sm font-medium opacity-90">{label}</div>
        </div>
    );
};

// Enhanced Claim Card Component
const ClaimCard = ({ claim, onVerify, onResolve }) => {
    const statusColors = {
        pending: 'bg-yellow-100 text-yellow-700 border-yellow-200',
        verified: 'bg-green-100 text-green-700 border-green-200',
        rejected: 'bg-red-100 text-red-700 border-red-200'
    };

    return (
        <Card className="overflow-hidden hover:shadow-lg transition-shadow">
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 px-4 sm:px-6 py-3 sm:py-4 border-b border-gray-200">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                    <div>
                        <h3 className="text-base sm:text-lg font-semibold text-gray-900">Claim #{claim.id}</h3>
                        <p className="text-xs sm:text-sm text-gray-600">For Item: {claim.item_title || `#${claim.item_id}`}</p>
                    </div>
                    <Badge className={`${statusColors[claim.status]} border self-start sm:self-auto`}>
                        {claim.status.toUpperCase()}
                    </Badge>
                </div>
            </div>

            <div className="p-4 sm:p-6">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                    <div>
                        <p className="text-xs sm:text-sm font-medium text-gray-500 mb-1">Claimed By</p>
                        <p className="font-medium text-sm sm:text-base">{claim.claimant_name || `User #${claim.claimant_id}`}</p>
                        <p className="text-xs sm:text-sm text-gray-500">{claim.claimant_email}</p>
                    </div>
                    <div>
                        <p className="text-xs sm:text-sm font-medium text-gray-500 mb-1">Submitted Date</p>
                        <p className="text-sm sm:text-base">{format(new Date(claim.created_at), 'MMM dd, yyyy HH:mm')}</p>
                    </div>
                </div>

                <div className="bg-gray-50 p-3 sm:p-4 rounded-lg mb-4">
                    <p className="text-xs sm:text-sm font-medium text-gray-700 mb-2">Proof Description</p>
                    <p className="text-xs sm:text-sm text-gray-600">{claim.proof_description}</p>
                </div>

                {claim.proof_image_url && (
                    <div className="mb-4">
                        <p className="text-xs sm:text-sm font-medium text-gray-700 mb-2">Proof Image</p>
                        <img
                            src={claim.proof_image_url}
                            alt="Proof"
                            className="h-32 sm:h-48 rounded-lg object-cover border w-full"
                        />
                    </div>
                )}

                <div className="flex flex-col sm:flex-row gap-2 sm:gap-3 pt-4 border-t">
                    {claim.status === 'pending' && (
                        <>
                            <Button
                                onClick={() => onVerify(claim.id, 'verified')}
                                className="w-full bg-green-600 hover:bg-green-700 text-white h-10 sm:h-11 text-sm sm:text-base"
                            >
                                <CheckCircle className="w-4 h-4 mr-2" />
                                Verify Claim
                            </Button>
                            <Button
                                onClick={() => onVerify(claim.id, 'rejected')}
                                variant="destructive"
                                className="w-full h-10 sm:h-11 text-sm sm:text-base"
                            >
                                <XCircle className="w-4 h-4 mr-2" />
                                Reject Claim
                            </Button>
                        </>
                    )}
                    {claim.status === 'verified' && (
                        <Button
                            onClick={() => onResolve(claim.item_id)}
                            className="w-full bg-blue-600 hover:bg-blue-700 h-10 sm:h-11 text-sm sm:text-base"
                        >
                            <CheckCircle className="w-4 h-4 mr-2" />
                            Mark as Resolved
                        </Button>
                    )}
                </div>
            </div>
        </Card>
    );
};

// History Claim Card (Read-only)
const HistoryClaimCard = ({ claim }) => {
    const statusColors = {
        verified: 'bg-green-100 text-green-700 border-green-200',
        rejected: 'bg-red-100 text-red-700 border-red-200'
    };

    return (
        <Card className="p-4 sm:p-6 hover:shadow-md transition-shadow">
            <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3">
                <div className="flex-1">
                    <div className="flex flex-col sm:flex-row sm:items-center gap-2 mb-3">
                        <h3 className="text-base sm:text-lg font-semibold text-gray-900">Claim #{claim.id}</h3>
                        <Badge className={`${statusColors[claim.status]} border self-start sm:self-auto`}>
                            {claim.status.toUpperCase()}
                        </Badge>
                    </div>
                    <p className="text-xs sm:text-sm text-gray-600 mb-3">For Item: {claim.item_title || `#${claim.item_id}`}</p>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div>
                            <p className="text-xs font-medium text-gray-500">Claimed By</p>
                            <p className="text-sm">{claim.claimant_name || `User #${claim.claimant_id}`}</p>
                        </div>
                        <div>
                            <p className="text-xs font-medium text-gray-500">Date</p>
                            <p className="text-sm">{format(new Date(claim.created_at), 'MMM dd, yyyy')}</p>
                        </div>
                    </div>
                </div>
                <Button
                    variant="outline"
                    size="sm"
                    onClick={() => window.open(`/items/${claim.item_id}`, '_blank')}
                    className="self-start sm:self-auto"
                >
                    <Eye className="w-4 h-4 mr-2" />
                    View Item
                </Button>
            </div>
        </Card>
    );
};

// Item Card Component
const ItemCard = ({ item, onResolve }) => {
    return (
        <Card className="p-4 sm:p-6 hover:shadow-md transition-shadow">
            <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
                <div className="flex gap-3 sm:gap-4 flex-1">
                    {item.images && item.images.length > 0 ? (
                        <img src={item.images[0].image_url} alt={item.title} className="w-16 h-16 sm:w-20 sm:h-20 object-cover rounded-md flex-shrink-0" />
                    ) : (
                        <div className="w-16 h-16 sm:w-20 sm:h-20 bg-gray-100 rounded-md flex items-center justify-center flex-shrink-0">
                            <Package className="w-6 h-6 sm:w-8 sm:h-8 text-gray-400" />
                        </div>
                    )}
                    <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-base sm:text-lg truncate">{item.title}</h3>
                        <p className="text-xs sm:text-sm text-gray-500 mb-2 truncate">{item.location}</p>
                        <div className="flex flex-wrap gap-2">
                            <Badge variant="outline" className="text-xs">{item.type}</Badge>
                            <Badge className={`text-xs ${item.status === 'resolved' ? 'bg-green-100 text-green-700' :
                                item.status === 'claimed' ? 'bg-yellow-100 text-yellow-700' :
                                    'bg-blue-100 text-blue-700'
                                }`}>{item.status}</Badge>
                        </div>
                    </div>
                </div>

                <div className="self-start sm:self-auto">
                    {item.status !== 'resolved' && (
                        <Button
                            onClick={() => onResolve(item.id)}
                            variant="outline"
                            size="sm"
                            className="text-green-600 border-green-200 hover:bg-green-50 w-full sm:w-auto"
                        >
                            <CheckCircle className="w-4 h-4 mr-2" />
                            Mark Resolved
                        </Button>
                    )}
                </div>
            </div>
        </Card>
    );
};

export default AdminDashboard;
