import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
    const isDark = ref(false)

    // Initialize theme
    function initTheme() {
        // Check localStorage
        const savedTheme = localStorage.getItem('theme')

        if (savedTheme) {
            isDark.value = savedTheme === 'dark'
        } else {
            // Check system preference
            isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
        }

        applyTheme()
    }

    // Toggle theme
    function toggleTheme() {
        isDark.value = !isDark.value
        applyTheme()
    }

    // Apply theme to document
    function applyTheme() {
        if (isDark.value) {
            document.documentElement.classList.add('dark')
            localStorage.setItem('theme', 'dark')
        } else {
            document.documentElement.classList.remove('dark')
            localStorage.setItem('theme', 'light')
        }
    }

    // Watch for system changes if no preference is saved
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!localStorage.getItem('theme')) {
            isDark.value = e.matches
            applyTheme()
        }
    })

    return {
        isDark,
        initTheme,
        toggleTheme,
    }
})
