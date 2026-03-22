<script lang="ts">
  import type { Component } from 'svelte';
  import { router } from './router.svelte.js';
  import { routeCache } from './routeCache.js';

  type RouteLoader = () => Promise<{ default: Component<{ params?: Record<string, string> }> }>;

  interface Props {
    routes: Record<string, RouteLoader>;
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
    for (const [pattern, loader] of Object.entries(routes)) {
      if (pattern === '*') continue;
      const { regex, paramNames } = patternToRegex(pattern);
      const m = location.match(regex);
      if (m) {
        const params: Record<string, string> = {};
        paramNames.forEach((name, i) => {
          params[name] = m[i + 1];
        });
        return { loader, params };
      }
    }
    const fallback = routes['*'];
    if (fallback) return { loader: fallback, params: {} };
    return null;
  }

  let CurrentComponent = $state<Component<{ params?: Record<string, string> }> | null>(null);
  let currentParams = $state<Record<string, string>>({});

  $effect(() => {
    const matched = matchRoute(router.location);
    if (!matched) {
      CurrentComponent = null;
      return;
    }

    const cached = routeCache.get(matched.loader);
    if (cached) {
      CurrentComponent = cached;
      currentParams = matched.params;
    } else {
      matched.loader()
        .then((module) => {
          routeCache.set(matched.loader, module.default);
          CurrentComponent = module.default;
          currentParams = matched.params;
        })
        .catch(() => {
          window.location.reload();
        });
    }
  });
</script>

{#if CurrentComponent}
  <CurrentComponent params={currentParams} />
{/if}
