import { useEffect, useMemo, useState } from 'react'
import axiosClient from '@/api/axiosClient'
import { Event, EventStatus } from '@/types'
import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Badge } from '@/components/ui/Badge'
import { motion } from 'framer-motion'

function formatDate(dt: string) {
  try {
    return new Date(dt).toLocaleString()
  } catch {
    return dt
  }
}

export default function DashboardPage() {
  const [events, setEvents] = useState<Event[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [title, setTitle] = useState('')
  const [startLocal, setStartLocal] = useState('')
  const [endLocal, setEndLocal] = useState('')
  const [creating, setCreating] = useState(false)

  async function loadEvents() {
    setLoading(true)
    setError(null)
    try {
      const res = await axiosClient.get<Event[]>('/events')
      setEvents(res.data)
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Failed to load events'
      setError(String(msg))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadEvents()
  }, [])

  async function onCreate(e: React.FormEvent) {
    e.preventDefault()
    if (!title || !startLocal || !endLocal) return
    setCreating(true)
    setError(null)
    try {
      const payload = {
        title,
        start_time: new Date(startLocal).toISOString(),
        end_time: new Date(endLocal).toISOString(),
      }
      const res = await axiosClient.post<Event>('/events', payload)
      setEvents((prev) => [res.data, ...prev])
      setTitle('')
      setStartLocal('')
      setEndLocal('')
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Failed to create event'
      setError(String(msg))
    } finally {
      setCreating(false)
    }
  }

  async function makeSwappable(id: string) {
    try {
      const target = events.find((e) => e.id === id)
      if (!target) return
      const res = await axiosClient.put<Event>(`/events/${id}`, { status: EventStatus.SWAPPABLE })
      setEvents((prev) => prev.map((e) => (e.id === id ? res.data : e)))
    } catch (err) {
      // silent fail with simple alert for now
      alert('Failed to update status')
    }
  }

  async function removeEvent(id: string) {
    try {
      await axiosClient.delete(`/events/${id}`)
      setEvents((prev) => prev.filter((e) => e.id !== id))
    } catch (err) {
      alert('Failed to delete')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">My Events</h1>
              <p className="text-gray-600 mt-1">Manage your schedule and availability</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <div className="text-2xl font-bold text-blue-600">{events.length}</div>
                <div className="text-sm text-gray-500">Total Events</div>
              </div>
            </div>
          </div>
        </div>

        {/* Create Event Form */}
        <Card className="mb-8 shadow-lg border-0 bg-white/95 backdrop-blur-sm">
          <div className="p-6">
            <div className="flex items-center mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg flex items-center justify-center mr-3">
                <span className="text-white font-bold">+</span>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Create New Event</h3>
                <p className="text-sm text-gray-600">Schedule a new meeting or appointment</p>
              </div>
            </div>
            
            <form onSubmit={onCreate} className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              <div className="lg:col-span-2">
                <label className="block text-sm font-semibold text-gray-700 mb-2">Event Title</label>
                <Input 
                  placeholder="e.g., Team Meeting, Client Call" 
                  value={title} 
                  onChange={(e) => setTitle(e.target.value)} 
                  required 
                  className="h-11 border-gray-300 focus:border-blue-600 focus:ring-blue-600"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Start Time</label>
                <Input 
                  type="datetime-local" 
                  value={startLocal} 
                  onChange={(e) => setStartLocal(e.target.value)} 
                  required 
                  className="h-11 border-gray-300 focus:border-blue-600 focus:ring-blue-600"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">End Time</label>
                <Input 
                  type="datetime-local" 
                  value={endLocal} 
                  onChange={(e) => setEndLocal(e.target.value)} 
                  required 
                  className="h-11 border-gray-300 focus:border-blue-600 focus:ring-blue-600"
                />
              </div>
              <div className="lg:col-span-4">
                <Button 
                  type="submit" 
                  loading={creating}
                  className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white shadow-lg hover:shadow-xl transition-all duration-200"
                >
                  {creating ? 'Creating Event…' : 'Create Event'}
                </Button>
              </div>
            </form>
            {error && (
              <motion.div 
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm mt-4"
              >
                {error}
              </motion.div>
            )}
          </div>
        </Card>

        {/* Events List */}
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="text-gray-600">Loading events...</div>
          </div>
        ) : events.length === 0 ? (
          <Card className="shadow-lg border-0 bg-white/95 backdrop-blur-sm">
            <div className="p-12 text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-gray-400 to-gray-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-white text-2xl">📅</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">No events yet</h3>
              <p className="text-gray-600">Create your first event to get started with scheduling</p>
            </div>
          </Card>
        ) : (
          <div className="space-y-6">
            {/* Events Table */}
            <Card className="shadow-lg border-0 bg-white/95 backdrop-blur-sm overflow-hidden">
              <div className="p-6 border-b border-gray-100">
                <h3 className="text-lg font-semibold text-gray-900">Your Events</h3>
                <p className="text-sm text-gray-600">Manage and organize your schedule</p>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Event</th>
                      <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Start Time</th>
                      <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">End Time</th>
                      <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Status</th>
                      <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {events.map((ev, index) => (
                      <motion.tr 
                        key={ev.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="hover:bg-blue-50/50 transition-colors"
                      >
                        <td className="px-6 py-4">
                          <div className="font-semibold text-gray-900">{ev.title}</div>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-600">
                          {formatDate(ev.start_time)}
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-600">
                          {formatDate(ev.end_time)}
                        </td>
                        <td className="px-6 py-4">
                          <Badge 
                            variant={
                              ev.status === EventStatus.SWAPPABLE ? 'success' :
                              ev.status === EventStatus.SWAP_PENDING ? 'warning' : 'secondary'
                            }
                            className="font-medium"
                          >
                            {ev.status === EventStatus.BUSY ? '🔒 Busy' :
                             ev.status === EventStatus.SWAPPABLE ? '🔄 Swappable' :
                             '⏳ Swap Pending'}
                          </Badge>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center space-x-2">
                            {ev.status === EventStatus.BUSY && (
                              <Button 
                                size="sm" 
                                onClick={() => makeSwappable(ev.id)}
                                className="bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white text-xs"
                              >
                                Make Swappable
                              </Button>
                            )}
                            <Button 
                              size="sm" 
                              variant="outline" 
                              onClick={() => removeEvent(ev.id)}
                              className="border-red-300 text-red-600 hover:bg-red-50 text-xs"
                            >
                              Delete
                            </Button>
                          </div>
                        </td>
                      </motion.tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>
          </div>
        )}
      </div>
    </div>
  )
}


