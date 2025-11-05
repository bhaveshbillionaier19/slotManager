import React from 'react';
import { motion } from 'framer-motion';

export const ModernIllustration: React.FC<{ className?: string }> = ({ className = "" }) => {
  return (
    <div className={`relative overflow-hidden ${className}`}>
      {/* Animated Background Shapes */}
      <div className="absolute inset-0">
        <motion.div
          className="absolute top-10 right-10 w-32 h-32 bg-gradient-to-br from-sky-200 to-indigo-200 rounded-full blur-xl opacity-60"
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
          className="absolute bottom-20 left-10 w-24 h-24 bg-gradient-to-br from-indigo-200 to-purple-200 rounded-full blur-xl opacity-40"
          animate={{ 
            scale: [1.2, 1, 1.2],
            x: [0, 20, 0]
          }}
          transition={{ 
            duration: 15,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
      </div>

      {/* Main SVG Illustration */}
      <svg
        viewBox="0 0 600 400"
        className="relative z-10 w-full h-full"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <linearGradient id="skyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#0EA5E9" />
            <stop offset="100%" stopColor="#3B82F6" />
          </linearGradient>
          <linearGradient id="carGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#6366F1" />
            <stop offset="100%" stopColor="#8B5CF6" />
          </linearGradient>
          <linearGradient id="buildingGrad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#F1F5F9" />
            <stop offset="100%" stopColor="#E2E8F0" />
          </linearGradient>
        </defs>

        {/* Background Sky */}
        <rect width="600" height="400" fill="url(#skyGrad)" opacity="0.1" />

        {/* Buildings/Office Background */}
        <g opacity="0.8">
          {/* Building 1 */}
          <rect x="50" y="150" width="80" height="200" rx="8" fill="url(#buildingGrad)" />
          <rect x="60" y="170" width="12" height="15" rx="2" fill="#3B82F6" opacity="0.3" />
          <rect x="80" y="170" width="12" height="15" rx="2" fill="#3B82F6" opacity="0.3" />
          <rect x="100" y="170" width="12" height="15" rx="2" fill="#3B82F6" opacity="0.3" />
          <rect x="60" y="200" width="12" height="15" rx="2" fill="#3B82F6" opacity="0.3" />
          <rect x="80" y="200" width="12" height="15" rx="2" fill="#3B82F6" opacity="0.3" />
          <rect x="100" y="200" width="12" height="15" rx="2" fill="#3B82F6" opacity="0.3" />

          {/* Building 2 */}
          <rect x="470" y="120" width="100" height="230" rx="8" fill="url(#buildingGrad)" />
          <rect x="485" y="140" width="15" height="18" rx="2" fill="#3B82F6" opacity="0.3" />
          <rect x="510" y="140" width="15" height="18" rx="2" fill="#3B82F6" opacity="0.3" />
          <rect x="535" y="140" width="15" height="18" rx="2" fill="#3B82F6" opacity="0.3" />
          <rect x="485" y="180" width="15" height="18" rx="2" fill="#3B82F6" opacity="0.3" />
          <rect x="510" y="180" width="15" height="18" rx="2" fill="#3B82F6" opacity="0.3" />
          <rect x="535" y="180" width="15" height="18" rx="2" fill="#3B82F6" opacity="0.3" />
        </g>

        {/* Road */}
        <rect x="0" y="320" width="600" height="80" fill="#64748B" opacity="0.2" />
        <rect x="0" y="355" width="600" height="4" fill="#FFFFFF" opacity="0.6" />

        {/* Parking Lot Grid */}
        <g stroke="#94A3B8" strokeWidth="2" opacity="0.4">
          <line x1="150" y1="280" x2="450" y2="280" />
          <line x1="150" y1="320" x2="450" y2="320" />
          <line x1="200" y1="260" x2="200" y2="320" />
          <line x1="250" y1="260" x2="250" y2="320" />
          <line x1="300" y1="260" x2="300" y2="320" />
          <line x1="350" y1="260" x2="350" y2="320" />
          <line x1="400" y1="260" x2="400" y2="320" />
        </g>

        {/* Cars in Parking */}
        <g>
          {/* Car 1 */}
          <motion.g
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.8 }}
          >
            <rect x="160" y="285" width="35" height="20" rx="8" fill="url(#carGrad)" />
            <rect x="165" y="288" width="8" height="6" rx="2" fill="#FFFFFF" opacity="0.8" />
            <rect x="182" y="288" width="8" height="6" rx="2" fill="#FFFFFF" opacity="0.8" />
            <circle cx="168" cy="308" r="4" fill="#1E293B" />
            <circle cx="187" cy="308" r="4" fill="#1E293B" />
          </motion.g>

          {/* Car 2 */}
          <motion.g
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7, duration: 0.8 }}
          >
            <rect x="260" y="285" width="35" height="20" rx="8" fill="#10B981" />
            <rect x="265" y="288" width="8" height="6" rx="2" fill="#FFFFFF" opacity="0.8" />
            <rect x="282" y="288" width="8" height="6" rx="2" fill="#FFFFFF" opacity="0.8" />
            <circle cx="268" cy="308" r="4" fill="#1E293B" />
            <circle cx="287" cy="308" r="4" fill="#1E293B" />
          </motion.g>

          {/* Car 3 */}
          <motion.g
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.9, duration: 0.8 }}
          >
            <rect x="360" y="285" width="35" height="20" rx="8" fill="#F59E0B" />
            <rect x="365" y="288" width="8" height="6" rx="2" fill="#FFFFFF" opacity="0.8" />
            <rect x="382" y="288" width="8" height="6" rx="2" fill="#FFFFFF" opacity="0.8" />
            <circle cx="368" cy="308" r="4" fill="#1E293B" />
            <circle cx="387" cy="308" r="4" fill="#1E293B" />
          </motion.g>
        </g>

        {/* People/Characters */}
        <g>
          {/* Person 1 */}
          <motion.g
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 1.1, duration: 0.6 }}
          >
            <circle cx="220" cy="250" r="8" fill="#FBBF24" />
            <rect x="215" y="258" width="10" height="18" rx="5" fill="#3B82F6" />
            <rect x="212" y="265" width="4" height="12" rx="2" fill="#FBBF24" />
            <rect x="224" y="265" width="4" height="12" rx="2" fill="#FBBF24" />
          </motion.g>

          {/* Person 2 */}
          <motion.g
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 1.3, duration: 0.6 }}
          >
            <circle cx="330" cy="250" r="8" fill="#F87171" />
            <rect x="325" y="258" width="10" height="18" rx="5" fill="#10B981" />
            <rect x="322" y="265" width="4" height="12" rx="2" fill="#F87171" />
            <rect x="334" y="265" width="4" height="12" rx="2" fill="#F87171" />
          </motion.g>
        </g>

        {/* Floating Icons */}
        <g opacity="0.6">
          <motion.g
            animate={{ y: [0, -10, 0] }}
            transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
          >
            <circle cx="480" cy="80" r="15" fill="#3B82F6" opacity="0.2" />
            <path d="M475 75 L480 80 L485 75 M480 75 L480 85" stroke="#3B82F6" strokeWidth="2" fill="none" />
          </motion.g>
          
          <motion.g
            animate={{ y: [0, -8, 0] }}
            transition={{ duration: 4, repeat: Infinity, ease: "easeInOut", delay: 1 }}
          >
            <circle cx="120" cy="100" r="12" fill="#10B981" opacity="0.2" />
            <rect x="115" y="95" width="10" height="10" rx="2" fill="#10B981" opacity="0.6" />
          </motion.g>
        </g>

        {/* Success Indicators */}
        <motion.g
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 1.5, duration: 0.5, type: "spring" }}
        >
          <circle cx="300" cy="180" r="20" fill="#10B981" opacity="0.9" />
          <path d="M292 180 L298 186 L308 174" stroke="white" strokeWidth="3" fill="none" strokeLinecap="round" strokeLinejoin="round" />
        </motion.g>
      </svg>

      {/* Overlay Text */}
      <motion.div
        className="absolute bottom-8 left-8 right-8 text-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.8, duration: 0.8 }}
      >
        <h3 className="text-2xl font-semibold text-slate-700 mb-2">
          Organize. Swap. Collaborate.
        </h3>
        <p className="text-slate-500 text-sm">
          Seamlessly manage your schedule with colleagues
        </p>
      </motion.div>
    </div>
  );
};
