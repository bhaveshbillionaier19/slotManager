import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { twMerge } from 'tailwind-merge';

const badgeVariants = cva(
  'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default:
          'border-transparent bg-blue-600 text-blue-50',
        secondary:
          'border-transparent bg-gray-200 text-gray-900',
        destructive:
          'border-transparent bg-red-500 text-red-50',
        success:
          'border-transparent bg-green-600 text-green-50',
        warning:
          'border-transparent bg-yellow-400 text-yellow-900',
        pending:
          'border-transparent bg-orange-500 text-orange-50',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={twMerge(badgeVariants({ variant }), className)} {...props} />
  );
}

export { Badge, badgeVariants };
