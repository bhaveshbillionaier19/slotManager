import { SwapRequestResponse } from '@/types';
import { Card } from './ui/Card';
import { Button } from './ui/Button';
import { ArrowRight, Check, X } from 'lucide-react';

function formatDate(dt?: string) {
  if (!dt) return '';
  try { 
    return new Date(dt).toLocaleString(undefined, { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
  } catch { return dt; }
}

interface IncomingRequestCardProps {
  request: SwapRequestResponse;
  onRespond: (id: string, accepted: boolean) => void;
  isResponding: boolean;
}

export function IncomingRequestCard({ request, onRespond, isResponding }: IncomingRequestCardProps) {
  const offered = request.offered_event_details;
  const requested = request.requested_event_details;

  return (
    <Card className="overflow-hidden">
      <div className="p-6">
        <p className="text-sm text-gray-600 mb-4">
          <span className="font-semibold text-gray-800">{request.requester_details?.name}</span> wants to swap slots with you.
        </p>
        <div className="flex items-center justify-center gap-2 sm:gap-4">
          <div className="flex-1 text-center bg-gray-50 p-3 sm:p-4 rounded-lg border">
            <p className="text-xs text-gray-500">They Offer</p>
            <p className="font-semibold text-gray-800 truncate">{offered?.title}</p>
            <p className="text-xs text-gray-500">{formatDate(offered?.start_time)}</p>
          </div>
          <ArrowRight className="text-gray-400 shrink-0" />
          <div className="flex-1 text-center bg-blue-50 p-3 sm:p-4 rounded-lg border border-blue-200">
            <p className="text-xs text-blue-700">You Give</p>
            <p className="font-semibold text-blue-900 truncate">{requested?.title}</p>
            <p className="text-xs text-blue-700">{formatDate(requested?.start_time)}</p>
          </div>
        </div>
      </div>
      <div className="bg-gray-50/70 p-3 border-t flex items-center justify-end gap-2">
        <Button variant="outline" size="sm" onClick={() => onRespond(request.id, false)} disabled={isResponding}>
          <X className="mr-1.5 h-4 w-4" />
          Decline
        </Button>
        <Button variant="default" size="sm" onClick={() => onRespond(request.id, true)} loading={isResponding}>
          <Check className="mr-1.5 h-4 w-4" />
          Accept
        </Button>
      </div>
    </Card>
  );
}
