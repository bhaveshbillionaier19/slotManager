import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import useAuth from '@/hooks/useAuth'
import axiosClient from '@/api/axiosClient'
import { Card } from '@/components/ui/Card'
import { Input } from '@/components/ui/Input'
import { Button } from '@/components/ui/Button'
import { motion } from 'framer-motion'

export default function SignupPage() {
  const navigate = useNavigate()
  const { login } = useAuth()

  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const res = await axiosClient.post('/auth/signup', { name, email, password })
      const token = res.data?.access_token
      if (!token) throw new Error('No token returned')
      login(token)
      navigate('/dashboard', { replace: true })
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Signup failed'
      setError(String(msg))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <motion.div 
          initial={{ opacity: 0, y: 20 }} 
          animate={{ opacity: 1, y: 0 }} 
          transition={{ type: 'spring', stiffness: 120, damping: 14 }}
        >
          {/* Header */}
          <div className="text-center mb-8">
            <div className="flex items-center justify-center mb-4">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg">
                <span className="text-white font-bold text-lg">S</span>
              </div>
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Join SlotSwapper</h1>
            <p className="text-gray-600">Make the most of your professional life</p>
          </div>

          {/* Signup Form */}
          <Card className="shadow-xl border-0 bg-white/95 backdrop-blur-sm">
            <div className="p-8">
              <form onSubmit={onSubmit} className="space-y-6">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Name</label>
                  <Input 
                    type="text" 
                    value={name} 
                    onChange={(e) => setName(e.target.value)} 
                    required 
                    placeholder="First and last name"
                    className="h-12 text-base border-gray-300 focus:border-blue-600 focus:ring-blue-600 rounded-lg"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Email</label>
                  <Input 
                    type="email" 
                    value={email} 
                    onChange={(e) => setEmail(e.target.value)} 
                    required 
                    placeholder="Email"
                    className="h-12 text-base border-gray-300 focus:border-blue-600 focus:ring-blue-600 rounded-lg"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Password (6+ characters)</label>
                  <Input 
                    type="password" 
                    value={password} 
                    onChange={(e) => setPassword(e.target.value)} 
                    required 
                    placeholder="Password"
                    className="h-12 text-base border-gray-300 focus:border-blue-600 focus:ring-blue-600 rounded-lg"
                  />
                </div>
                
                {error && (
                  <motion.div 
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm"
                  >
                    {error}
                  </motion.div>
                )}


                <Button 
                  type="submit" 
                  className="w-full h-12 text-base font-semibold bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-lg hover:shadow-xl transition-all duration-200 rounded-lg" 
                  loading={loading}
                >
                  {loading ? 'Creating account…' : 'Join'}
                </Button>
              </form>

              <div className="mt-8 text-center">
                <p className="text-gray-600">
                  Already on SlotSwapper?{' '}
                  <Link to="/login" className="text-blue-600 hover:text-blue-700 font-semibold hover:underline">
                    Sign in
                  </Link>
                </p>
              </div>
            </div>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}


