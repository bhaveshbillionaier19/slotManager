import { IncomingRequestCard } from '@/components/IncomingRequestCard'
import { OutgoingRequestCard } from '@/components/OutgoingRequestCard'
import axiosClient from '@/api/axiosClient'
import { SwapRequestResponse, SwapRequestStatus } from '@/types'
import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { motion, AnimatePresence } from 'framer-motion'

export default function RequestsPage() {
  const [incoming, setIncoming] = useState<SwapRequestResponse[]>([])
  const [outgoing, setOutgoing] = useState<SwapRequestResponse[]>([])
  const [loadingIn, setLoadingIn] = useState(false)
  const [loadingOut, setLoadingOut] = useState(false)
  const [errIn, setErrIn] = useState<string | null>(null)
  const [errOut, setErrOut] = useState<string | null>(null)
  const [actingId, setActingId] = useState<string | null>(null)
  const [tab, setTab] = useState<'incoming' | 'outgoing'>('incoming')

  async function loadIncoming() {
    setLoadingIn(true); setErrIn(null)
    try {
      const res = await axiosClient.get<SwapRequestResponse[]>('/swaps/incoming-requests')
      setIncoming(res.data)
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Failed to load incoming requests'
      setErrIn(String(msg))
    } finally {
      setLoadingIn(false)
    }
  }

  async function loadOutgoing() {
    setLoadingOut(true); setErrOut(null)
    try {
      const res = await axiosClient.get<SwapRequestResponse[]>('/swaps/outgoing-requests')
      setOutgoing(res.data)
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Failed to load outgoing requests'
      setErrOut(String(msg))
    } finally {
      setLoadingOut(false)
    }
  }

  useEffect(() => {
    loadIncoming(); loadOutgoing()
  }, [])

  async function respond(id: string, accepted: boolean) {
    setActingId(id)
    try {
      await axiosClient.post(`/swaps/response-swap/${id}`, { accepted })
      setIncoming((prev) => prev.filter((r) => r.id !== id))
      loadOutgoing()
    } catch (err: any) {
      alert(err?.response?.data?.detail || err?.message || 'Failed to respond')
    } finally {
      setActingId(null)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-white to-teal-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Swap Requests</h1>
              <p className="text-gray-600 mt-1">Manage your incoming and outgoing swap requests</p>
            </div>
            <div className="flex items-center space-x-6">
              <div className="text-right">
                <div className="text-2xl font-bold text-emerald-600">{incoming.length}</div>
                <div className="text-sm text-gray-500">Incoming</div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-teal-600">{outgoing.length}</div>
                <div className="text-sm text-gray-500">Outgoing</div>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <Card className="mb-8 shadow-lg border-0 bg-white/95 backdrop-blur-sm">
          <div className="p-6">
            <nav className="flex space-x-8">
              <button
                className={`flex items-center px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 ${
                  tab === 'incoming' 
                    ? 'bg-gradient-to-r from-emerald-500 to-green-500 text-white shadow-lg' 
                    : 'text-gray-600 hover:text-emerald-600 hover:bg-emerald-50'
                }`}
                onClick={() => setTab('incoming')}
              >
                <div className="w-6 h-6 bg-emerald-100 rounded-full flex items-center justify-center mr-2">
                  <span className="text-emerald-600 text-xs">📥</span>
                </div>
                Incoming Requests
                {incoming.length > 0 && (
                  <span className={`ml-2 px-2 py-1 rounded-full text-xs ${
                    tab === 'incoming' ? 'bg-white/20 text-white' : 'bg-emerald-100 text-emerald-600'
                  }`}>
                    {incoming.length}
                  </span>
                )}
              </button>
              <button
                className={`flex items-center px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 ${
                  tab === 'outgoing' 
                    ? 'bg-gradient-to-r from-teal-500 to-cyan-500 text-white shadow-lg' 
                    : 'text-gray-600 hover:text-teal-600 hover:bg-teal-50'
                }`}
                onClick={() => setTab('outgoing')}
              >
                <div className="w-6 h-6 bg-teal-100 rounded-full flex items-center justify-center mr-2">
                  <span className="text-teal-600 text-xs">📤</span>
                </div>
                Outgoing Requests
                {outgoing.length > 0 && (
                  <span className={`ml-2 px-2 py-1 rounded-full text-xs ${
                    tab === 'outgoing' ? 'bg-white/20 text-white' : 'bg-teal-100 text-teal-600'
                  }`}>
                    {outgoing.length}
                  </span>
                )}
              </button>
            </nav>
          </div>
        </Card>

        {/* Content */}
        <AnimatePresence mode="wait">
          {tab === 'incoming' ? (
            <motion.div
              key="incoming"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ type: 'spring', stiffness: 120, damping: 14 }}
            >
              {loadingIn ? (
                <div className="flex items-center justify-center py-12">
                  <div className="text-gray-600">Loading incoming requests...</div>
                </div>
              ) : errIn ? (
                <Card className="shadow-lg border-0 bg-white/95 backdrop-blur-sm">
                  <div className="p-8 text-center">
                    <div className="w-16 h-16 bg-gradient-to-r from-red-400 to-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
                      <span className="text-white text-2xl">⚠️</span>
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Requests</h3>
                    <p className="text-red-600">{errIn}</p>
                  </div>
                </Card>
              ) : incoming.length === 0 ? (
                <Card className="shadow-lg border-0 bg-white/95 backdrop-blur-sm">
                  <div className="p-12 text-center">
                    <div className="w-16 h-16 bg-gradient-to-r from-emerald-400 to-green-400 rounded-full flex items-center justify-center mx-auto mb-4">
                      <span className="text-white text-2xl">📥</span>
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">No incoming requests</h3>
                    <p className="text-gray-600">You'll see swap requests from other users here</p>
                  </div>
                </Card>
              ) : (
                <div className="grid gap-6 lg:grid-cols-2">
                  {incoming.map((r, index) => (
                    <motion.div
                      key={r.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <IncomingRequestCard request={r} onRespond={respond} isResponding={actingId === r.id} />
                    </motion.div>
                  ))}
                </div>
              )}
            </motion.div>
          ) : (
            <motion.div
              key="outgoing"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ type: 'spring', stiffness: 120, damping: 14 }}
            >
              {loadingOut ? (
                <div className="flex items-center justify-center py-12">
                  <div className="text-gray-600">Loading outgoing requests...</div>
                </div>
              ) : errOut ? (
                <Card className="shadow-lg border-0 bg-white/95 backdrop-blur-sm">
                  <div className="p-8 text-center">
                    <div className="w-16 h-16 bg-gradient-to-r from-red-400 to-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
                      <span className="text-white text-2xl">⚠️</span>
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Requests</h3>
                    <p className="text-red-600">{errOut}</p>
                  </div>
                </Card>
              ) : outgoing.length === 0 ? (
                <Card className="shadow-lg border-0 bg-white/95 backdrop-blur-sm">
                  <div className="p-12 text-center">
                    <div className="w-16 h-16 bg-gradient-to-r from-teal-400 to-cyan-400 rounded-full flex items-center justify-center mx-auto mb-4">
                      <span className="text-white text-2xl">📤</span>
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">No outgoing requests</h3>
                    <p className="text-gray-600">Visit the marketplace to request swaps with colleagues</p>
                  </div>
                </Card>
              ) : (
                <div className="grid gap-6 lg:grid-cols-2">
                  {outgoing.map((r, index) => (
                    <motion.div
                      key={r.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <OutgoingRequestCard request={r} />
                    </motion.div>
                  ))}
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}


