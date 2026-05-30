/**
 * Campus Bridge - Unified Theme Manager
 * Handles switching between Light (Emerald/White) and Dark (Gold/Black) themes.
 * Persists user preference in LocalStorage.
 * Zero database logic/Python code changes.
 */

class ThemeManager {
  constructor() {
    this.THEMES = {
      LIGHT: 'light',
      DARK: 'dark'
    };
    this.STORAGE_KEY = 'campus-bridge-theme';
    this.init();
  }

  init() {
    // Get saved theme from localStorage or default to light
    const savedTheme = localStorage.getItem(this.STORAGE_KEY) || this.THEMES.LIGHT;
    this.setTheme(savedTheme);
    
    // Inject the theme switcher button when DOM is fully interactive
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        this.createToggleButton();
      });
    } else {
      this.createToggleButton();
    }
  }

  setTheme(theme) {
    if (!Object.values(this.THEMES).includes(theme)) {
      theme = this.THEMES.LIGHT;
    }

    // Set theme on html element as data attribute for CSS to pick up
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(this.STORAGE_KEY, theme);

    // Update toggle button icon
    this.updateToggleIcon(theme);
  }

  toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || this.THEMES.LIGHT;
    const newTheme = currentTheme === this.THEMES.LIGHT ? this.THEMES.DARK : this.THEMES.LIGHT;
    this.setTheme(newTheme);
  }

  getCurrentTheme() {
    return document.documentElement.getAttribute('data-theme') || this.THEMES.LIGHT;
  }

  createToggleButton() {
    // Check if button already exists in the HTML to avoid duplicates
    if (document.querySelector('.theme-toggle')) {
      return;
    }

    const button = document.createElement('button');
    button.className = 'theme-toggle';
    button.setAttribute('title', 'Switch Theme');
    button.setAttribute('aria-label', 'Toggle light and dark theme');
    button.innerHTML = this.getToggleIcon(this.getCurrentTheme());

    button.addEventListener('click', (e) => {
      e.preventDefault();
      this.toggleTheme();
    });

    document.body.appendChild(button);
  }

  updateToggleIcon(theme) {
    const button = document.querySelector('.theme-toggle');
    if (button) {
      button.innerHTML = this.getToggleIcon(theme);
    }
  }

  getToggleIcon(theme) {
    // Light theme button shows Moon (to go to dark)
    // Dark theme button shows Sun (to go to light)
    return theme === this.THEMES.LIGHT ? '🌙' : '☀️';
  }
}

// Instantiate immediately to apply the theme class as fast as possible (prevents flash)
const campusBridgeThemeManager = new ThemeManager();
