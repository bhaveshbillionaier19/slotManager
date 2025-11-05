import { useState, useEffect } from 'react';
import axiosClient from '@/api/axiosClient';
import useAuth from '@/hooks/useAuth';
import { SwapRequestResponse } from '@/types';

export function useNotifications() {
  const [hasNotifications, setHasNotifications] = useState(false);
  const [notificationCount, setNotificationCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const { token } = useAuth();

  const checkNotifications = async () => {
    if (!token) {
      setHasNotifications(false);
      setNotificationCount(0);
      return;
    }

    try {
      setLoading(true);
      const response = await axiosClient.get('/swaps/incoming-requests');
      const incomingRequests: SwapRequestResponse[] = response.data;
      
      // Count pending requests (not accepted/declined)
      const pendingRequests = incomingRequests.filter(
        request => request.status === 'PENDING'
      );
      
      setNotificationCount(pendingRequests.length);
      setHasNotifications(pendingRequests.length > 0);
    } catch (error) {
      console.error('Failed to fetch notifications:', error);
      setHasNotifications(false);
      setNotificationCount(0);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!token) {
      setHasNotifications(false);
      setNotificationCount(0);
      return;
    }

    // Check notifications on mount and when token changes
    checkNotifications();

    // Set up polling every 30 seconds to check for new notifications
    const interval = setInterval(checkNotifications, 30000);

    return () => clearInterval(interval);
  }, [token]);

  return {
    hasNotifications,
    notificationCount,
    loading,
    refreshNotifications: checkNotifications
  };
}
