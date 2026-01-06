/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                cyber: {
                    black: '#0a0a0a',
                    dark: '#111111',
                    panel: 'rgba(10, 10, 10, 0.8)',
                    cyan: '#00f3ff',
                    green: '#0aff00',
                    red: '#ff003c',
                    muted: '#2a2a2a'
                }
            },
            backgroundImage: {
                'grid-pattern': "linear-gradient(to right, #1a1a1a 1px, transparent 1px), linear-gradient(to bottom, #1a1a1a 1px, transparent 1px)",
            },
            fontFamily: {
                mono: ['"Fira Code"', 'monospace'],
                display: ['"Rajdhani"', 'sans-serif']
            },
            boxShadow: {
                'neon-cyan': '0 0 5px #00f3ff, 0 0 20px rgba(0, 243, 255, 0.3)',
                'neon-green': '0 0 5px #0aff00, 0 0 20px rgba(10, 255, 0, 0.3)',
                'neon-red': '0 0 5px #ff003c, 0 0 20px rgba(255, 0, 60, 0.3)',
            }
        },
    },
    plugins: [],
}
