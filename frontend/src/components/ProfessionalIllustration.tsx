import React from 'react';

export const ProfessionalIllustration: React.FC<{ className?: string }> = ({ className = "" }) => {
  return (
    <div className={`relative ${className}`}>
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-linkedin-50 via-blue-50 to-indigo-50 rounded-3xl"></div>
      
      {/* Professional SVG Illustration */}
      <svg
        viewBox="0 0 800 600"
        className="relative z-10 w-full h-full"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Background elements */}
        <defs>
          <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#0ea5e9" stopOpacity="0.1" />
            <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.1" />
          </linearGradient>
          <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#0ea5e9" />
            <stop offset="100%" stopColor="#3b82f6" />
          </linearGradient>
        </defs>
        
        {/* Abstract background shapes */}
        <circle cx="650" cy="100" r="80" fill="url(#grad1)" />
        <circle cx="700" cy="500" r="60" fill="url(#grad1)" />
        <rect x="50" y="450" width="100" height="100" rx="20" fill="url(#grad1)" />
        
        {/* Main illustration - Professional person with laptop */}
        <g transform="translate(200, 80)">
          {/* Desk */}
          <rect x="0" y="400" width="400" height="20" rx="10" fill="#e5e7eb" />
          
          {/* Laptop */}
          <g transform="translate(100, 300)">
            {/* Laptop base */}
            <rect x="0" y="80" width="200" height="120" rx="8" fill="#374151" />
            {/* Laptop screen */}
            <rect x="10" y="0" width="180" height="90" rx="6" fill="#1f2937" />
            {/* Screen content */}
            <rect x="20" y="10" width="160" height="70" rx="4" fill="#f3f4f6" />
            {/* Screen elements */}
            <rect x="30" y="20" width="60" height="8" rx="4" fill="url(#grad2)" />
            <rect x="30" y="35" width="140" height="4" rx="2" fill="#d1d5db" />
            <rect x="30" y="45" width="100" height="4" rx="2" fill="#d1d5db" />
            <rect x="30" y="55" width="120" height="4" rx="2" fill="#d1d5db" />
          </g>
          
          {/* Person */}
          <g transform="translate(150, 150)">
            {/* Head */}
            <circle cx="50" cy="40" r="30" fill="#fbbf24" />
            {/* Hair */}
            <path d="M25 25 Q50 10 75 25 Q75 15 50 15 Q25 15 25 25" fill="#92400e" />
            {/* Body */}
            <rect x="25" y="65" width="50" height="80" rx="25" fill="#3b82f6" />
            {/* Arms */}
            <rect x="5" y="75" width="20" height="60" rx="10" fill="#fbbf24" />
            <rect x="75" y="75" width="20" height="60" rx="10" fill="#fbbf24" />
            {/* Hands */}
            <circle cx="15" cy="140" r="8" fill="#fbbf24" />
            <circle cx="85" cy="140" r="8" fill="#fbbf24" />
          </g>
          
          {/* Floating elements - representing connectivity/networking */}
          <g opacity="0.6">
            {/* Network nodes */}
            <circle cx="50" cy="150" r="8" fill="url(#grad2)" />
            <circle cx="350" cy="200" r="8" fill="url(#grad2)" />
            <circle cx="300" cy="100" r="8" fill="url(#grad2)" />
            <circle cx="80" cy="250" r="8" fill="url(#grad2)" />
            
            {/* Connecting lines */}
            <line x1="50" y1="150" x2="300" y2="100" stroke="url(#grad2)" strokeWidth="2" opacity="0.5" />
            <line x1="300" y1="100" x2="350" y2="200" stroke="url(#grad2)" strokeWidth="2" opacity="0.5" />
            <line x1="50" y1="150" x2="80" y2="250" stroke="url(#grad2)" strokeWidth="2" opacity="0.5" />
          </g>
          
          {/* Success indicators */}
          <g transform="translate(320, 120)">
            <circle cx="0" cy="0" r="15" fill="#10b981" />
            <path d="M-6 0 L-2 4 L6 -4" stroke="white" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
          </g>
          
          <g transform="translate(60, 120)">
            <circle cx="0" cy="0" r="15" fill="#10b981" />
            <path d="M-6 0 L-2 4 L6 -4" stroke="white" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
          </g>
        </g>
        
        {/* Decorative elements */}
        <g opacity="0.3">
          <circle cx="100" cy="100" r="4" fill="#3b82f6" />
          <circle cx="720" cy="300" r="6" fill="#0ea5e9" />
          <circle cx="150" cy="500" r="5" fill="#6366f1" />
        </g>
      </svg>
    </div>
  );
};
