import { useEffect, useMemo, useState } from 'react'
import axiosClient from '@/api/axiosClient'
import { Event, EventStatus, SwappableEventResponse, SwapRequestCreate } from '@/types'
import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { RequestSwapModal } from '@/components/RequestSwapModal'
import { motion } from 'framer-motion'

function formatDate(dt: string) {
  try {
    return new Date(dt).toLocaleString()
  } catch {
    return dt
  }
}

export default function MarketplacePage() {
  const [swappable, setSwappable] = useState<SwappableEventResponse[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [chooserOpen, setChooserOpen] = useState(false)
  const [targetSlot, setTargetSlot] = useState<SwappableEventResponse | null>(null)

  async function loadSwappable() {
    setLoading(true)
    setError(null)
    try {
      const res = await axiosClient.get<SwappableEventResponse[]>('/swaps/swappable-slots')
      setSwappable(res.data)
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Failed to load marketplace slots'
      setError(String(msg))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadSwappable()
  }, [])

  function openChooser(theirId: string) {
    const target = swappable.find(s => s.id === theirId) || null
    setTargetSlot(target)
    setChooserOpen(true)
  }

  function closeChooser() {
    setChooserOpen(false)
    setTargetSlot(null)
  }

  async function handleSuccess() {
    closeChooser()
    await loadSwappable()
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Marketplace</h1>
              <p className="text-gray-600 mt-1">Discover and swap available time slots with colleagues</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <div className="text-2xl font-bold text-purple-600">{swappable.length}</div>
                <div className="text-sm text-gray-500">Available Slots</div>
              </div>
            </div>
          </div>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="text-gray-600">Loading marketplace...</div>
          </div>
        ) : error ? (
          <Card className="shadow-lg border-0 bg-white/95 backdrop-blur-sm">
            <div className="p-8 text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-red-400 to-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-white text-2xl">⚠️</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Marketplace</h3>
              <p className="text-red-600">{error}</p>
            </div>
          </Card>
        ) : swappable.length === 0 ? (
          <Card className="shadow-lg border-0 bg-white/95 backdrop-blur-sm">
            <div className="p-12 text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-white text-2xl">🏪</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">No slots available</h3>
              <p className="text-gray-600">Check back later for new swappable time slots</p>
            </div>
          </Card>
        ) : (
          <div className="space-y-6">
            {/* Marketplace Grid */}
            <motion.div layout className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {swappable.map((slot, index) => (
                <motion.div 
                  key={slot.id} 
                  initial={{ opacity: 0, y: 20 }} 
                  animate={{ opacity: 1, y: 0 }} 
                  transition={{ delay: index * 0.1, type: 'spring', stiffness: 120, damping: 14 }}
                >
                  <Card className="shadow-lg border-0 bg-white/95 backdrop-blur-sm transition-all duration-300 hover:scale-105 hover:shadow-xl group cursor-pointer">
                    <div className="p-6">
                      {/* Slot Header */}
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex-1">
                          <h3 className="font-bold text-lg text-gray-900 group-hover:text-purple-600 transition-colors truncate">
                            {slot.title}
                          </h3>
                          <div className="flex items-center mt-1">
                            <div className="w-6 h-6 bg-gradient-to-r from-blue-400 to-indigo-400 rounded-full flex items-center justify-center mr-2">
                              <span className="text-white text-xs font-bold">
                                {slot.owner_name.charAt(0).toUpperCase()}
                              </span>
                            </div>
                            <span className="text-sm text-gray-600">{slot.owner_name}</span>
                          </div>
                        </div>
                        <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                          <span className="text-white text-lg">🔄</span>
                        </div>
                      </div>

                      {/* Time Details */}
                      <div className="space-y-3 mb-6">
                        <div className="flex items-center text-sm">
                          <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center mr-3">
                            <span className="text-green-600 text-xs">▶️</span>
                          </div>
                          <div>
                            <div className="font-medium text-gray-900">Start</div>
                            <div className="text-gray-600">{formatDate(slot.start_time)}</div>
                          </div>
                        </div>
                        <div className="flex items-center text-sm">
                          <div className="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center mr-3">
                            <span className="text-red-600 text-xs">⏹️</span>
                          </div>
                          <div>
                            <div className="font-medium text-gray-900">End</div>
                            <div className="text-gray-600">{formatDate(slot.end_time)}</div>
                          </div>
                        </div>
                      </div>

                      {/* Action Button */}
                      <Button 
                        onClick={() => openChooser(slot.id)}
                        className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg hover:shadow-xl transition-all duration-200 group-hover:scale-105"
                      >
                        Request Swap
                      </Button>
                    </div>
                  </Card>
                </motion.div>
              ))}
            </motion.div>
          </div>
        )}

        <RequestSwapModal isOpen={chooserOpen} onClose={closeChooser} targetSlot={targetSlot} onSuccess={handleSuccess} />
      </div>
    </div>
  )
}
