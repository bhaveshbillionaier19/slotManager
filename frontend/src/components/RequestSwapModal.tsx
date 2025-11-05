import { useEffect, useState } from 'react';
import axiosClient from '@/api/axiosClient';
import { Event, EventStatus, SwapRequestCreate, SwappableEventResponse } from '@/types';
import { Modal } from './ui/Modal';
import { Button } from './ui/Button';
import { Spinner } from './ui/Spinner';

interface RequestSwapModalProps {
  isOpen: boolean;
  onClose: () => void;
  targetSlot: SwappableEventResponse | null;
  onSuccess: () => void;
}

function formatDate(dt: string) {
  try {
    return new Date(dt).toLocaleString(undefined, { dateStyle: 'short', timeStyle: 'short' });
  } catch { return dt; }
}

export function RequestSwapModal({ isOpen, onClose, targetSlot, onSuccess }: RequestSwapModalProps) {
  const [mySwappable, setMySwappable] = useState<Event[]>([]);
  const [myChoice, setMyChoice] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [requesting, setRequesting] = useState(false);

  useEffect(() => {
    if (!isOpen) return;

    async function loadMySwappable() {
      setLoading(true);
      setError(null);
      setMyChoice('');
      try {
        // The backend supports filtering by status, so we can rely on this
        const res = await axiosClient.get<Event[]>('/events', { params: { status: EventStatus.SWAPPABLE } });
        setMySwappable(res.data.filter(e => e.status === EventStatus.SWAPPABLE));
      } catch (err: any) {
        setError(err?.response?.data?.detail || 'Failed to load your swappable slots');
      } finally {
        setLoading(false);
      }
    }
    loadMySwappable();
  }, [isOpen]);

  async function handleConfirmSwap() {
    if (!targetSlot || !myChoice) return;
    setRequesting(true);
    setError(null);
    try {
      const payload: SwapRequestCreate = { my_slot_id: myChoice, their_slot_id: targetSlot.id };
      await axiosClient.post('/swaps/request-swap', payload);
      onSuccess();
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to request swap');
    } finally {
      setRequesting(false);
    }
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`Request Swap for "${targetSlot?.title}"`}>
      <div className="mt-4 space-y-4">
        <p className="text-sm text-gray-600">Select one of your available slots to offer in exchange.</p>
        
        {loading && <div className="flex justify-center py-4"><Spinner /></div>}
        
        {error && <div className="text-sm text-red-600 bg-red-50 p-3 rounded-md">{error}</div>}

        {!loading && !error && (
          <div className="max-h-60 overflow-y-auto space-y-2 rounded-lg border border-gray-200 p-2 bg-gray-50/50">
            {mySwappable.length === 0 ? (
              <p className="text-sm text-gray-500 text-center py-8">You have no swappable slots available.</p>
            ) : (
              mySwappable.map((e) => (
                <label
                  key={e.id}
                  className={`flex items-center p-3 rounded-md cursor-pointer transition-colors ${
                    myChoice === e.id ? 'bg-blue-100 border border-blue-300' : 'bg-white hover:bg-gray-100 border border-transparent'
                  }`}
                >
                  <input
                    type="radio"
                    name="mySlot"
                    value={e.id}
                    checked={myChoice === e.id}
                    onChange={() => setMyChoice(e.id)}
                    className="h-4 w-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                  />
                  <div className="ml-3 text-sm">
                    <p className="font-medium text-gray-900">{e.title}</p>
                    <p className="text-gray-500">{formatDate(e.start_time)}</p>
                  </div>
                </label>
              ))
            )}
          </div>
        )}

        <div className="flex justify-end gap-2 pt-4">
          <Button variant="outline" onClick={onClose} disabled={requesting}>Cancel</Button>
          <Button onClick={handleConfirmSwap} disabled={!myChoice || requesting || loading} loading={requesting}>
            Confirm & Request
          </Button>
        </div>
      </div>
    </Modal>
  );
}
