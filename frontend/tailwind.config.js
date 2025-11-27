/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // SIGOT Brand Identity v3.0
        // Primary: Color casi negro elegante y profesional
        // El logo conceptual es una "S" estilizada que sugiere una carretera/conexión
        primary: {
          50: '#f5f5f5',   // Gris muy claro
          100: '#e5e5e5',  // Gris claro
          200: '#d4d4d4',  // Gris medio-claro
          300: '#a3a3a3',  // Gris medio
          400: '#737373',  // Gris medio-oscuro
          500: '#1a1a1a',  // Color principal - casi negro
          600: '#171717',  // Casi negro más oscuro
          700: '#141414',  // Casi negro
          800: '#111111',  // Muy oscuro
          900: '#0a0a0a',  // Casi negro puro
          DEFAULT: '#1a1a1a', // Casi negro profesional SIGOT
        },
        // Secondary: Gris neutro elegante para elementos secundarios
        secondary: {
          50: '#f9fafb',
          100: '#f3f4f6',
          200: '#e5e7eb',
          300: '#d1d5db',
          400: '#9ca3af',
          500: '#6b7280',
          600: '#4b5563',
          700: '#374151',
          800: '#1f2937',
          900: '#111827',
          DEFAULT: '#6b7280',
        },
        // Chat bubble colors - estilo WhatsApp (mantenemos los colores originales)
        'chat-bubble-me': '#DCF8C6', // Verde claro WhatsApp
        'chat-bubble-other': '#FFFFFF', // Blanco para mensajes recibidos
        // Amarillo obra (obra yellow)
        'obra': {
          50: '#fefce8',   // Amarillo muy claro
          100: '#fef9c3',  // Amarillo claro
          200: '#fef08a',  // Amarillo medio-claro
          300: '#fde047',  // Amarillo medio
          400: '#facc15',  // Amarillo obra claro
          500: '#eab308',  // Amarillo obra
          600: '#ca8a04',  // Amarillo obra oscuro
          700: '#a16207',  // Amarillo obra más oscuro
          800: '#854d0e',  // Amarillo obra muy oscuro
          900: '#713f12',  // Amarillo obra casi marrón
          DEFAULT: '#facc15', // Amarillo obra claro por defecto
        },
      },
      fontFamily: {
        sans: [
          '-apple-system',
          'BlinkMacSystemFont',
          '"Segoe UI"',
          'Roboto',
          '"Helvetica Neue"',
          'Arial',
          'sans-serif',
        ],
        saviko: ['Saviko Sans', 'sans-serif'],
      },
      boxShadow: {
        'sigot': '0 2px 8px rgba(0, 0, 0, 0.08)',
        'sigot-lg': '0 4px 16px rgba(0, 0, 0, 0.12)',
      },
    },
  },
  plugins: [],
}
