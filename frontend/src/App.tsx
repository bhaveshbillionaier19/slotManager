import { Navigate, Route, Routes, useLocation } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import DashboardPage from './pages/DashboardPage'
import MarketplacePage from './pages/MarketplacePage'
import RequestsPage from './pages/RequestsPage'
import { NavBar } from './components/NavBar'
import { AnimatePresence, motion } from 'framer-motion'

function AnimatedPageContainer({ children }: { children: React.ReactNode }) {
  return (
    <motion.main
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -8 }}
      transition={{ type: 'spring', stiffness: 120, damping: 14 }}
      className="min-h-[calc(100vh-4rem)] bg-gradient-to-b from-white to-gray-50"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">{children}</div>
    </motion.main>
  )
}

export default function App() {
  const location = useLocation()
  return (
    <AuthProvider>
      <NavBar />
      <AnimatePresence mode="wait">
        <Routes location={location} key={location.pathname}>
          <Route path="/login" element={<AnimatedPageContainer><LoginPage /></AnimatedPageContainer>} />
          <Route path="/signup" element={<AnimatedPageContainer><SignupPage /></AnimatedPageContainer>} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <AnimatedPageContainer>
                  <DashboardPage />
                </AnimatedPageContainer>
              </ProtectedRoute>
            }
          />
          <Route
            path="/marketplace"
            element={
              <ProtectedRoute>
                <AnimatedPageContainer>
                  <MarketplacePage />
                </AnimatedPageContainer>
              </ProtectedRoute>
            }
          />
          <Route
            path="/requests"
            element={
              <ProtectedRoute>
                <AnimatedPageContainer>
                  <RequestsPage />
                </AnimatedPageContainer>
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AnimatePresence>
    </AuthProvider>
  )
}


