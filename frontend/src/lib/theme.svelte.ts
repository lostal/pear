type Theme = 'light' | 'dark' | 'system';

function createTheme() {
  let theme = $state<Theme>('system');
  let mediaQuery: MediaQueryList | undefined;
  let isListeningToSystem = false;

  function updateDom(isDark: boolean) {
    const contains = document.documentElement.classList.contains('dark');
    if (isDark && !contains) {
      document.documentElement.classList.add('dark');
    } else if (!isDark && contains) {
      document.documentElement.classList.remove('dark');
    }
  }

  const onSystemThemeChange = (e: MediaQueryListEvent) => {
    if (isListeningToSystem) updateDom(e.matches);
  };

  function applyTheme(newTheme: Theme) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('ipear_theme', newTheme);

    if (!mediaQuery) {
      mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    }
    mediaQuery.removeEventListener('change', onSystemThemeChange);

    if (newTheme === 'system') {
      isListeningToSystem = true;
      updateDom(mediaQuery.matches);
      mediaQuery.addEventListener('change', onSystemThemeChange);
    } else {
      isListeningToSystem = false;
      updateDom(newTheme === 'dark');
    }
  }

  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('ipear_theme') as Theme | null;
    const initial =
      saved && ['light', 'dark', 'system'].includes(saved) ? saved : 'light';
    theme = initial;
    applyTheme(initial);
  }

  function set(newTheme: Theme) {
    theme = newTheme;
    applyTheme(newTheme);
  }

  return {
    get current() { return theme; },
    set,
  };
}

export const theme = createTheme();
