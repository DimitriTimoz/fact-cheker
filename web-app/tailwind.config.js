/** @type {import('tailwindcss').Config} */
export default {
  content: [],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1E3A8A', // Bleu foncé
          light: '#3B82F6',  // Bleu clair
        },
        secondary: {
          DEFAULT: '#F59E0B', // Orange
          light: '#FDE68A',  // Jaune clair
        },
        success: '#10B981',   // Vert pour la vérification
        error: '#EF4444',     // Rouge pour les erreurs
        background: {
          light: '#F3F4F6',   // Gris clair pour le fond
          DEFAULT: '#FFFFFF', // Blanc
        },
        text: {
          DEFAULT: '#111827', // Gris foncé pour le texte
          muted: '#6B7280',   // Gris plus clair pour le texte secondaire
        },
      },
    },
  },
  plugins: [],
}

