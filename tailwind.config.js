/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        paper: {
          50: '#FCFCFB',
          100: '#F7F7F4',
          200: '#EFEFEA',
          300: '#E5E5DF',
          400: '#D5D5CD',
        },
        charcoal: {
          950: '#0E0F12',
          900: '#121316',
          800: '#1E2025',
          700: '#2C2E35',
          600: '#454852',
          500: '#646875',
          400: '#8A8E9B',
          300: '#B5B8C2',
        },
        risk: {
          low: {
            DEFAULT: '#10B981',
            soft: '#059669',
            light: '#ECFDF5',
            border: '#A7F3D0',
          },
          moderate: {
            DEFAULT: '#F59E0B',
            soft: '#D97706',
            light: '#FFFBEB',
            border: '#FDE68A',
          },
          high: {
            DEFAULT: '#F97316',
            soft: '#EA580C',
            light: '#FFF7ED',
            border: '#FED7AA',
          },
          critical: {
            DEFAULT: '#EF4444',
            soft: '#DC2626',
            light: '#FEF2F2',
            border: '#FECACA',
          },
        },
      },
      fontFamily: {
        sans: [
          'Plus Jakarta Sans',
          'Inter',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'sans-serif',
        ],
        mono: [
          'JetBrains Mono',
          'ui-monospace',
          'SFMono-Regular',
          'Menlo',
          'monospace',
        ],
      },
      boxShadow: {
        'subtle': '0 1px 2px 0 rgba(0, 0, 0, 0.03), 0 1px 6px -1px rgba(0, 0, 0, 0.02)',
        'elevated': '0 4px 20px -2px rgba(0, 0, 0, 0.05), 0 2px 6px -1px rgba(0, 0, 0, 0.02)',
        'floating': '0 12px 36px -4px rgba(0, 0, 0, 0.08), 0 4px 12px -2px rgba(0, 0, 0, 0.03)',
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.25rem',
        '3xl': '1.75rem',
      },
      animation: {
        'pulse-subtle': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float-slow': 'float 8s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-8px)' },
        },
      },
    },
  },
  plugins: [],
}
