import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import axiosClient from '@/api/axiosClient'
import { Input } from '@/components/ui/Input'
import { Button } from '@/components/ui/Button'
import { Toast } from '@/components/ui/Toast'
import { ModernIllustration } from '@/components/ModernIllustration'
import useAuth from '@/hooks/useAuth'
import { motion } from 'framer-motion'
import { Calendar, Clock, ArrowRight } from 'lucide-react'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showToast, setShowToast] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  const { login } = useAuth()

  const from = location.state?.from?.pathname || '/dashboard'

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    
    try {
      const res = await axiosClient.post('/auth/login', { email, password })
      const token = res.data.access_token
      
      // Use the auth context login function to properly set the token and user state
      login(token)
      
      // Show success toast
      setShowToast(true)
      
      // Navigate to the intended page after a short delay
      setTimeout(() => {
        navigate(from, { replace: true })
      }, 1000)
      
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Login failed'
      setError(String(msg))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-100 via-white to-indigo-100 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-20 left-20 w-64 h-64 bg-gradient-to-br from-sky-200 to-indigo-200 rounded-full blur-3xl opacity-20"
          animate={{ 
            scale: [1, 1.2, 1],
            rotate: [0, 180, 360]
          }}
          transition={{ 
            duration: 20,
            repeat: Infinity,
            ease: "linear"
          }}
        />
        <motion.div
          className="absolute bottom-20 right-20 w-48 h-48 bg-gradient-to-br from-indigo-200 to-purple-200 rounded-full blur-3xl opacity-20"
          animate={{ 
            scale: [1.2, 1, 1.2],
            x: [0, 50, 0],
            y: [0, -30, 0]
          }}
          transition={{ 
            duration: 15,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        
        {/* Decorative Icons */}
        <motion.div
          className="absolute top-32 right-32 text-sky-300 opacity-30"
          animate={{ y: [0, -20, 0] }}
          transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
        >
          <Calendar size={32} />
        </motion.div>
        <motion.div
          className="absolute bottom-32 left-32 text-indigo-300 opacity-30"
          animate={{ y: [0, -15, 0] }}
          transition={{ duration: 5, repeat: Infinity, ease: "easeInOut", delay: 2 }}
        >
          <Clock size={28} />
        </motion.div>
        <motion.div
          className="absolute top-1/2 left-16 text-purple-300 opacity-30"
          animate={{ rotate: [0, 360] }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
        >
          <ArrowRight size={24} />
        </motion.div>
      </div>

      {/* Main Container - Centered */}
      <div className="w-full max-w-6xl mx-auto flex items-center justify-center min-h-[80vh]">
        {/* Main Card Container */}
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ type: 'spring', stiffness: 120, damping: 14 }}
          className="w-full max-w-5xl bg-white/95 backdrop-blur-lg rounded-3xl shadow-2xl border border-white/20 overflow-hidden relative z-10"
        >
          <div className="grid grid-cols-1 lg:grid-cols-2 min-h-[700px]">
            {/* Left Side - Login Form */}
            <div className="p-8 lg:p-12 flex flex-col justify-center bg-white/50 backdrop-blur-sm">
              <div className="max-w-md mx-auto w-full">
                {/* Brand Logo */}
                <motion.div 
                  className="text-center mb-10"
                  initial={{ opacity: 0, y: -20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                >
                  <Link to="/" className="inline-flex items-center space-x-3 justify-center">
                    <div className="w-12 h-12 bg-gradient-to-r from-sky-500 to-indigo-500 rounded-2xl flex items-center justify-center shadow-lg">
                      <span className="text-white font-bold text-xl">S</span>
                    </div>
                    <span className="text-2xl font-bold text-slate-900">SlotSwapper</span>
                  </Link>
                </motion.div>

                {/* Welcome Header */}
                <div className="text-center mb-10">
                  <motion.h1 
                    className="text-4xl font-bold text-gray-900 mb-4 leading-tight"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                  >
                    Welcome Back
                  </motion.h1>
                  <motion.p 
                    className="text-lg text-gray-600"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                  >
                    Sign in to manage and swap meetings easily
                  </motion.p>
                </div>

                {/* Login Form */}
                <motion.form 
                  onSubmit={onSubmit} 
                  className="space-y-6"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                >
                  <div>
                    <Input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="Email or phone"
                      required
                      className="w-full h-14 border-2 border-gray-200 rounded-xl px-4 py-4 text-base focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 transition-all duration-200 bg-white/80"
                    />
                  </div>

                  <div>
                    <Input
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="Password"
                      required
                      showPasswordToggle
                      className="w-full h-14 border-2 border-gray-200 rounded-xl px-4 py-4 text-base focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 transition-all duration-200 bg-white/80"
                    />
                  </div>

                  {error && (
                    <motion.div 
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      className="bg-red-50 border-2 border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm font-medium"
                    >
                      {error}
                    </motion.div>
                  )}

                  <Button
                    type="submit"
                    loading={loading}
                    className="w-full h-14 bg-gradient-to-r from-sky-500 to-indigo-500 text-white font-semibold text-lg rounded-xl shadow-lg hover:shadow-xl hover:scale-[1.02] transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-indigo-200"
                  >
                    {loading ? 'Signing in...' : 'Sign In'}
                  </Button>
                </motion.form>

                {/* Divider */}
                <div className="relative my-8">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t-2 border-gray-200" />
                  </div>
                  <div className="relative flex justify-center text-sm">
                    <span className="px-6 bg-white text-gray-500 font-semibold">or</span>
                  </div>
                </div>

                {/* Join Now Button */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.6 }}
                >
                  <Link to="/signup">
                    <Button
                      variant="outline"
                      className="w-full h-14 border-2 border-gray-300 text-gray-700 font-semibold text-lg rounded-xl hover:bg-gray-50 hover:border-gray-400 transition-all duration-200"
                    >
                      Join now
                    </Button>
                  </Link>
                </motion.div>

              </div>
            </div>

            {/* Right Side - Illustration */}
            <div className="hidden lg:flex items-center justify-center bg-gradient-to-br from-sky-50 to-indigo-100 relative">
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.5, type: 'spring', stiffness: 120, damping: 14 }}
                className="w-full h-full p-8"
              >
                <ModernIllustration className="w-full h-full" />
              </motion.div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Toast Notification */}
      <Toast
        isVisible={showToast}
        onClose={() => setShowToast(false)}
        message="Login successful! Redirecting... 🎉"
        type="success"
      />
    </div>
  )
}
