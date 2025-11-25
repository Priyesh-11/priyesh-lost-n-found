import { formatDistanceToNow, format, parseISO } from 'date-fns';

/**
 * Formats a date to relative time (e.g., "2 days ago")
 * Falls back to absolute date if over 30 days old
 */
export const formatRelativeTime = (dateString) => {
    if (!dateString) return 'Date unknown';

    try {
        const date = typeof dateString === 'string' ? parseISO(dateString) : new Date(dateString);
        const now = new Date();
        const daysDiff = Math.floor((now - date) / (1000 * 60 * 60 * 24));

        // If more than 30 days old, show absolute date
        if (daysDiff > 30) {
            return format(date, 'MMM dd, yyyy');
        }

        // Otherwise show relative time
        return formatDistanceToNow(date, { addSuffix: true });
    } catch (e) {
        return 'Date unknown';
    }
};

/**
 * Get status color classes
 */
export const getStatusColor = (status) => {
    const colors = {
        active: 'bg-green-100 text-green-700 border-green-200',
        claimed: 'bg-yellow-100 text-yellow-700 border-yellow-200',
        resolved: 'bg-gray-100 text-gray-700 border-gray-200',
        pending: 'bg-blue-100 text-blue-700 border-blue-200'
    };

    return colors[status?.toLowerCase()] || colors.active;
};

/**
 * Get status label
 */
export const getStatusLabel = (status) => {
    const labels = {
        active: 'Active',
        claimed: 'Claimed',
        resolved: 'Resolved',
        pending: 'Pending'
    };

    return labels[status?.toLowerCase()] || status;
};
