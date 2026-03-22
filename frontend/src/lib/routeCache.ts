import type { Component } from 'svelte';

type RouteLoader = () => Promise<{ default: Component<any> }>;

export const routeCache = new Map<RouteLoader, Component<any>>();

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
