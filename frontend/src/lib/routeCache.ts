import type { Component } from 'svelte';

type PageComponent = Component<{ params?: Record<string, string> }>;
type RouteLoader = () => Promise<{ default: PageComponent }>;

export const routeCache = new Map<RouteLoader, PageComponent>();

export async function preloadRoutes(loaders: RouteLoader[]) {
  await Promise.all(
    loaders.map(async (loader) => {
      if (!routeCache.has(loader)) {
        const module = await loader();
        routeCache.set(loader, module.default);
      }
    })
  );
}
