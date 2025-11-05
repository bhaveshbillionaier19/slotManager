import { SwapRequestResponse, SwapRequestStatus } from '@/types';
import { Card } from './ui/Card';
import { Badge } from './ui/Badge';
import { ArrowRight } from 'lucide-react';

function formatDate(dt?: string) {
  if (!dt) return '';
  try { 
    return new Date(dt).toLocaleString(undefined, { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
  } catch { return dt; }
}

const statusMap: Record<SwapRequestStatus, { text: string; variant: 'success' | 'warning' | 'pending' | 'destructive' }> = {
  [SwapRequestStatus.PENDING]: { text: 'Pending', variant: 'pending' },
  [SwapRequestStatus.ACCEPTED]: { text: 'Accepted', variant: 'success' },
  [SwapRequestStatus.REJECTED]: { text: 'Rejected', variant: 'destructive' },
};

interface OutgoingRequestCardProps {
  request: SwapRequestResponse;
}

export function OutgoingRequestCard({ request }: OutgoingRequestCardProps) {
  const offered = request.offered_event_details;
  const requested = request.requested_event_details;

  return (
    <Card className="overflow-hidden">
      <div className="p-6">
        <div className="flex items-center justify-between mb-4">
            <p className="text-sm text-gray-600">
                Your swap request
            </p>
            <Badge variant={statusMap[request.status]?.variant || 'secondary'}>
                {statusMap[request.status]?.text || request.status}
            </Badge>
        </div>
        <div className="flex items-center justify-center gap-2 sm:gap-4">
          <div className="flex-1 text-center bg-blue-50 p-3 sm:p-4 rounded-lg border border-blue-200">
            <p className="text-xs text-blue-700">You Offer</p>
            <p className="font-semibold text-blue-900 truncate">{offered?.title}</p>
            <p className="text-xs text-blue-700">{formatDate(offered?.start_time)}</p>
          </div>
          <ArrowRight className="text-gray-400 shrink-0" />
          <div className="flex-1 text-center bg-gray-50 p-3 sm:p-4 rounded-lg border">
            <p className="text-xs text-gray-500">You Request</p>
            <p className="font-semibold text-gray-800 truncate">{requested?.title}</p>
            <p className="text-xs text-gray-500">{formatDate(requested?.start_time)}</p>
          </div>
        </div>
      </div>
    </Card>
  );
}
