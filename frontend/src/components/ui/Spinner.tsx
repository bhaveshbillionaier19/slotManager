import { Loader2 } from 'lucide-react';
import { twMerge } from 'tailwind-merge';

interface SpinnerProps {
  className?: string;
  size?: number;
}

export function Spinner({ className, size = 24 }: SpinnerProps) {
  return (
    <Loader2
      size={size}
      className={twMerge('animate-spin text-blue-600', className)}
    />
  );
}
