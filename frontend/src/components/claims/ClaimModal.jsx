import React, { useState } from 'react';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Textarea } from '../ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '../ui/dialog';
import { Upload, X, Loader2 } from 'lucide-react';
import { useToast } from '../../hooks/use-toast';
import { claimsService, itemsService } from '../../services/api';

const ClaimModal = ({ isOpen, onClose, itemId, itemTitle, onSuccess }) => {
    const { toast } = useToast();
    const [description, setDescription] = useState('');
    const [image, setImage] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            setImage(file);
            setImagePreview(URL.createObjectURL(file));
        }
    };

    const removeImage = () => {
        setImage(null);
        setImagePreview(null);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!description) {
            toast({
                title: "Error",
                description: "Please provide a description or proof details.",
                variant: "destructive"
            });
            return;
        }

        setLoading(true);
        try {
            let imageUrl = null;

            // Upload image if provided
            if (image) {
                const formData = new FormData();
                // Backend expects 'files' as List[UploadFile], so we append it correctly
                // Use the dedicated claim proof upload endpoint
                formData.append('files', image);

                const uploadRes = await itemsService.uploadClaimProof(itemId, formData);
                if (uploadRes.uploaded && uploadRes.uploaded.length > 0) {
                    imageUrl = uploadRes.uploaded[0];
                }
            }

            await claimsService.create(itemId, {
                proof_description: description,
                proof_image_url: imageUrl
            });

            toast({
                title: "Claim Submitted",
                description: "Your claim has been submitted for verification.",
            });
            onSuccess();
            onClose();
        } catch (error) {
            console.error("Claim submission error:", error);
            toast({
                title: "Error",
                description: error.response?.data?.detail || "Failed to submit claim.",
                variant: "destructive"
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-md">
                <DialogHeader>
                    <DialogTitle>Claim Item: {itemTitle}</DialogTitle>
                    <DialogDescription>
                        Provide proof that this item belongs to you. This will be reviewed by an administrator.
                    </DialogDescription>
                </DialogHeader>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="space-y-2">
                        <Label htmlFor="description">Proof Description *</Label>
                        <Textarea
                            id="description"
                            placeholder="Describe unique features, contents, or where you lost it..."
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            rows={4}
                        />
                    </div>

                    <div className="space-y-2">
                        <Label>Proof Image (Optional)</Label>
                        {!imagePreview ? (
                            <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-blue-500 transition-colors">
                                <input
                                    type="file"
                                    accept="image/*"
                                    onChange={handleImageUpload}
                                    className="hidden"
                                    id="claim-image-upload"
                                />
                                <label htmlFor="claim-image-upload" className="cursor-pointer block">
                                    <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                                    <span className="text-sm text-gray-600">Upload matching image or receipt</span>
                                </label>
                            </div>
                        ) : (
                            <div className="relative">
                                <img
                                    src={imagePreview}
                                    alt="Proof Preview"
                                    className="w-full h-48 object-cover rounded-lg"
                                />
                                <button
                                    type="button"
                                    onClick={removeImage}
                                    className="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600"
                                >
                                    <X className="w-4 h-4" />
                                </button>
                            </div>
                        )}
                    </div>

                    <DialogFooter>
                        <Button type="button" variant="outline" onClick={onClose}>
                            Cancel
                        </Button>
                        <Button type="submit" disabled={loading}>
                            {loading ? (
                                <>
                                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                    Submitting...
                                </>
                            ) : (
                                'Submit Claim'
                            )}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
};

export default ClaimModal;
