import { useState } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { Button } from './ui/Button'; // Assuming this is your custom Button component
import useAuth from '@/hooks/useAuth'; // Assuming this hook provides token and logout
import { useNotifications } from '@/hooks/useNotifications';
import { Toast } from './ui/Toast';
import { LogOut, Menu, X, Home, ShoppingBag, MessageSquare, User, Bell } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// --- Configuration ---
const navLinks = [
  { href: '/dashboard', label: 'Dashboard', icon: Home }, // Changed 'Home' to 'Dashboard' for more professional feel
  { href: '/marketplace', label: 'Marketplace', icon: ShoppingBag },
  { href: '/requests', label: 'Requests', icon: MessageSquare },
];

export function NavBar() {
  const { token, logout } = useAuth();
  const { hasNotifications, notificationCount } = useNotifications();
  const [isOpen, setIsOpen] = useState(false);
  const [showLogoutToast, setShowLogoutToast] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    setShowLogoutToast(true);
    // Close mobile menu if open
    setIsOpen(false);
    // Navigate to login page after a short delay
    setTimeout(() => {
      navigate('/login', { replace: true });
    }, 1000);
  };

  const getLinkClassName = ({ isActive }: { isActive: boolean }) =>
    `flex items-center space-x-2 md:flex-col md:space-x-0 md:space-y-1 px-3 py-2 text-sm font-medium transition-colors duration-200 rounded-lg group ${ 
      isActive
        ? 'text-indigo-700 bg-indigo-50' // Deeper indigo for active state
        : 'text-gray-600 hover:text-indigo-700 hover:bg-indigo-50'
    }`;

  // Logged-Out State Navbar
  if (!token) {
    return (
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center space-x-3">
              <div className="w-9 h-9 bg-indigo-600 rounded-full flex items-center justify-center shadow-md">
                <span className="text-white font-extrabold text-lg">S</span>
              </div>
              <span className="text-xl font-bold text-gray-900 tracking-tight">SlotSwapper</span>
            </Link>
            
            <div className="flex items-center space-x-2">
              <Link to="/login">
                <Button variant="ghost" className="text-gray-600 hover:text-indigo-600 px-4">
                  Sign in
                </Button>
              </Link>
              <Link to="/signup">
                <Button className="bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-500/50 transition-all duration-300 transform hover:scale-[1.02]">
                  Join now
                </Button>
              </Link>
            </div>
          </div>
        </nav>
      </header>
    );
  }

  // Logged-In State Navbar
  return (
    <header className="bg-white border-b border-gray-100 sticky top-0 z-50">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo */}
          <Link to="/dashboard" className="flex items-center space-x-3">
            <div className="w-9 h-9 bg-indigo-600 rounded-full flex items-center justify-center shadow-md">
              <span className="text-white font-extrabold text-lg">S</span>
            </div>
            <span className="text-xl font-bold text-gray-900 tracking-tight">SlotSwapper</span>
          </Link>
          
          {/* Desktop Nav Links (Centred) */}
          <div className="hidden md:flex items-center space-x-2 h-full">
            {navLinks.map((link) => {
              const Icon = link.icon;
              return (
                <NavLink key={link.href} to={link.href} className={getLinkClassName}>
                  <Icon className="w-5 h-5" />
                  <span className="text-xs">{link.label}</span> 
                </NavLink>
              );
            })}
          </div>

          {/* Desktop User Menu & Sign out */}
          <div className="hidden md:flex items-center space-x-4">
            {/* Notification Button */}
            <Link to="/requests" className="relative">
              <button className="p-2 rounded-full text-gray-600 hover:text-indigo-600 hover:bg-indigo-50 transition-colors duration-200 relative">
                <Bell className="w-6 h-6" />
                {hasNotifications && (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center"
                  >
                    <span className="text-xs font-bold text-white">
                      {notificationCount > 9 ? '9+' : notificationCount}
                    </span>
                  </motion.div>
                )}
                {hasNotifications && (
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                    className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full opacity-75"
                  />
                )}
              </button>
            </Link>

            {/* Aesthetic Avatar Placeholder */}
            <div className="w-9 h-9 bg-gray-200 rounded-full flex items-center justify-center border-2 border-indigo-500/50">
              <User className="w-5 h-5 text-gray-500" />
            </div>
            
            <Button 
              variant="outline" 
              size="sm" 
              onClick={handleLogout}
              className="border-gray-300 text-gray-600 hover:bg-red-50 hover:border-red-400 hover:text-red-700 transition-colors"
            >
              <LogOut className="mr-2 h-4 w-4" />
              Sign out
            </Button>
          </div>
          
          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center">
            <button onClick={() => setIsOpen(!isOpen)} className="p-2 rounded-md text-gray-700 hover:bg-gray-100 transition-colors">
              <span className="sr-only">Open main menu</span>
              {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </nav>

      {/* Mobile menu (Animated with Framer Motion) */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ type: 'tween', duration: 0.2 }}
            className="md:hidden border-t border-gray-200 bg-white shadow-xl"
          >
            <div className="pt-4 pb-3 space-y-1">
                {/* Mobile Avatar */}
                <div className="flex items-center justify-between px-4 mb-3">
                    <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center border-2 border-indigo-500/50">
                            <User className="w-5 h-5 text-gray-500" />
                        </div>
                        <span className="font-semibold text-gray-800">User Profile</span>
                    </div>
                    
                    {/* Mobile Notification Button */}
                    <Link to="/requests" className="relative" onClick={() => setIsOpen(false)}>
                        <button className="p-2 rounded-full text-gray-600 hover:text-indigo-600 hover:bg-indigo-50 transition-colors duration-200 relative">
                            <Bell className="w-6 h-6" />
                            {hasNotifications && (
                                <motion.div
                                    initial={{ scale: 0 }}
                                    animate={{ scale: 1 }}
                                    className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center"
                                >
                                    <span className="text-xs font-bold text-white">
                                        {notificationCount > 9 ? '9+' : notificationCount}
                                    </span>
                                </motion.div>
                            )}
                        </button>
                    </Link>
                </div>
                
                {/* Mobile Nav Links */}
                {navLinks.map((link) => {
                    const Icon = link.icon;
                    return (
                        <NavLink 
                            key={link.href} 
                            to={link.href} 
                            className={({ isActive }) => 
                                `flex items-center space-x-4 px-4 py-3 mx-2 rounded-lg transition-colors ${
                                    isActive 
                                        ? 'bg-indigo-50 text-indigo-700 font-semibold' 
                                        : 'text-gray-700 hover:bg-gray-50'
                                }`
                            } 
                            onClick={() => setIsOpen(false)}
                        >
                            <Icon className="w-5 h-5" />
                            <span>{link.label}</span>
                        </NavLink>
                    );
                })}
            </div>
            
            {/* Mobile Sign out */}
            <div className="pt-4 pb-4 border-t border-gray-100 px-4">
              <Button 
                variant="outline" 
                onClick={handleLogout} 
                className="w-full justify-center border-red-300 text-red-600 hover:bg-red-50 hover:text-red-700 transition-colors"
              >
                <LogOut className="mr-2 h-4 w-4" />
                Sign out
              </Button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Logout Toast Notification */}
      <Toast
        isVisible={showLogoutToast}
        onClose={() => setShowLogoutToast(false)}
        message="Successfully logged out! Redirecting to login... 👋"
        type="success"
      />
    </header>
  );
}