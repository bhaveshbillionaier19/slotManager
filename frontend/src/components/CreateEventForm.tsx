import { useState } from 'react';
import axiosClient from '@/api/axiosClient';
import { Event } from '@/types';
import { Button } from './ui/Button';
import { Input } from './ui/Input';

interface CreateEventFormProps {
  onSuccess: (newEvent: Event) => void;
}

export function CreateEventForm({ onSuccess }: CreateEventFormProps) {
  const [title, setTitle] = useState('');
  const [startLocal, setStartLocal] = useState('');
  const [endLocal, setEndLocal] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!title || !startLocal || !endLocal) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const payload = {
        title,
        start_time: new Date(startLocal).toISOString(),
        end_time: new Date(endLocal).toISOString(),
      };
      const res = await axiosClient.post<Event>('/events', payload);
      // Clear form and call parent success handler
      setTitle('');
      setStartLocal('');
      setEndLocal('');
      onSuccess(res.data);
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Failed to create event';
      setError(String(msg));
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 pt-2">
      <div className="space-y-2">
        <label htmlFor="title" className="text-sm font-medium text-gray-700">Title</label>
        <Input
          id="title"
          placeholder="e.g., Weekly Team Sync"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>
      <div className="space-y-2">
        <label htmlFor="start_time" className="text-sm font-medium text-gray-700">Start Time</label>
        <Input
          id="start_time"
          type="datetime-local"
          value={startLocal}
          onChange={(e) => setStartLocal(e.target.value)}
          required
        />
      </div>
      <div className="space-y-2">
        <label htmlFor="end_time" className="text-sm font-medium text-gray-700">End Time</label>
        <Input
          id="end_time"
          type="datetime-local"
          value={endLocal}
          onChange={(e) => setEndLocal(e.target.value)}
          required
        />
      </div>
      
      {error && (
        <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md p-3">
          {error}
        </div>
      )}

      <div className="flex justify-end pt-2">
        <Button type="submit" loading={loading}>
          Create Event
        </Button>
      </div>
    </form>
  );
}
