<script lang="ts">
  import { router } from './router.svelte.js';

  interface Props {
    routes: Record<string, any>;
  }

  let { routes }: Props = $props();

  function patternToRegex(pattern: string) {
    const paramNames: string[] = [];
    const regexStr = pattern.replace(/:([^/]+)/g, (_, name) => {
      paramNames.push(name);
      return '([^/]+)';
    });
    return { regex: new RegExp(`^${regexStr}/?$`), paramNames };
  }

  function matchRoute(location: string) {
    for (const [pattern, Component] of Object.entries(routes)) {
      if (pattern === '*') continue;
      const { regex, paramNames } = patternToRegex(pattern);
      const m = location.match(regex);
      if (m) {
        const params: Record<string, string> = {};
        paramNames.forEach((name, i) => { params[name] = m[i + 1]; });
        return { Component, params };
      }
    }
    const fallback = routes['*'];
    if (fallback) return { Component: fallback, params: {} };
    return null;
  }

  const matched = $derived(matchRoute(router.location));
</script>

{#if matched}
  {@const { Component, params } = matched}
  <Component {params} />
{/if}
