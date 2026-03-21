<script lang="ts">
  import { onMount } from 'svelte';
  import { push } from 'svelte-spa-router';
  import { animate, inView } from 'motion';
  import { auth } from '../stores/auth.svelte.js';

  let heroHeight = $state('100svh');
  let heroContent: HTMLElement | undefined = $state();
  let showcaseA: HTMLElement | undefined = $state();
  let showcaseB: HTMLElement | undefined = $state();
  let ctaSection: HTMLElement | undefined = $state();

  onMount(() => {
    const navbar = document.getElementById('site-header');
    if (navbar) {
      heroHeight = `calc(100svh - ${navbar.offsetHeight}px)`;
    }

    if (heroContent) {
      const children = heroContent.querySelectorAll('.hero-child');
      children.forEach((el, i) => {
        animate(el, { opacity: [0, 1], y: [20, 0] }, { duration: 0.5, delay: i * 0.12 });
      });
    }

    if (showcaseA) {
      inView(showcaseA, () => {
        const textEl = showcaseA!.querySelector('.showcase-text');
        const imgEl = showcaseA!.querySelector('.showcase-img');
        if (textEl) animate(textEl, { opacity: [0, 1], x: [-50, 0] }, { duration: 0.6 });
        if (imgEl) animate(imgEl, { opacity: [0, 1], x: [50, 0] }, { duration: 0.6, delay: 0.1 });
      });
    }

    if (showcaseB) {
      inView(showcaseB, () => {
        const imgEl = showcaseB!.querySelector('.showcase-img');
        const textEl = showcaseB!.querySelector('.showcase-text');
        if (imgEl) animate(imgEl, { opacity: [0, 1], x: [-50, 0] }, { duration: 0.6 });
        if (textEl) animate(textEl, { opacity: [0, 1], x: [50, 0] }, { duration: 0.6, delay: 0.1 });
      });
    }

    if (ctaSection) {
      inView(ctaSection, () => {
        const children = ctaSection!.querySelectorAll('.cta-child');
        animate(children, { opacity: [0, 1], y: [30, 0] }, { delay: 0.1, duration: 0.5 });
      });
    }
  });
</script>

<!-- S1: Hero -->
<section
  class="flex flex-col items-center justify-center text-center px-6 relative overflow-hidden"
  style="height: {heroHeight}; background-color: var(--color-background);"
>
  <!-- Collage de fondo -->
  <img
    src="/collage.png"
    alt=""
    aria-hidden="true"
    class="absolute inset-0 w-full h-full object-cover object-center select-none pointer-events-none"
    style="opacity: 0.4;"
  />
  <!-- Overlay gradiente para legibilidad del texto y transición perfecta al fondo -->
  <div
    class="absolute inset-0 pointer-events-none"
    style="background: linear-gradient(to bottom, rgba(252,252,249,0.05) 0%, rgba(252,252,249,0.65) 45%, rgba(252,252,249,0.95) 80%, #fcfcf9 100%);"
  ></div>

  <!-- Contenido -->
  <div bind:this={heroContent} class="relative z-10 flex flex-col items-center">
    <h1
      class="hero-child mb-4 max-w-4xl"
      style="opacity:0; font-family: var(--font-serif); font-style: italic; font-weight: 400; font-size: clamp(3rem, 8vw, 6rem); line-height: 1.05; letter-spacing: -0.01em; color: var(--color-foreground);"
    >
      Pear.
    </h1>

    <p
      class="hero-child text-lg mb-10 max-w-md"
      style="opacity:0; color: var(--color-muted-foreground); line-height: 1.6;"
    >
      Un futuro de la pera.
    </p>

    <div class="hero-child" style="opacity:0;">
      {#if auth.isAuthenticated}
        <button
          class="inline-flex items-center justify-center font-medium text-sm px-6 py-2.5 rounded-md transition-opacity hover:opacity-90 cursor-pointer"
          style="background: var(--color-primary); color: var(--color-primary-foreground);"
          onclick={() => push('/products')}
        >
          Descubrir
        </button>
      {:else}
        <button
          class="inline-flex items-center justify-center font-medium text-sm px-6 py-2.5 rounded-md transition-opacity hover:opacity-90 cursor-pointer"
          style="background: var(--color-primary); color: var(--color-primary-foreground);"
          onclick={() => push('/login')}
        >
          Iniciar sesión
        </button>
      {/if}
    </div>
  </div>
</section>

<!-- S3: iPear — texto izquierda, imagen derecha -->
<section
  bind:this={showcaseA}
  class="py-24 px-6"
  style="background-color: var(--color-background);"
>
  <div class="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
    <div class="showcase-text" style="opacity:0;">
      <p class="text-xs font-medium mb-3 tracking-widest uppercase" style="color: var(--color-muted-foreground);">iPear</p>
      <h2 class="text-3xl sm:text-4xl font-black mb-5" style="line-height: 1.1;">
        El teléfono que muerde diferente.
      </h2>
      <p class="leading-relaxed" style="color: var(--color-muted-foreground);">
        Diseñado desde cero para que cada interacción se sienta como hincarle el diente a algo que de verdad vale la pena.
      </p>
    </div>
    <div
      class="showcase-img aspect-square rounded-2xl overflow-hidden"
      style="opacity:0; background: var(--color-secondary);"
    >
      <img src="/ipear.png" alt="iPear" class="w-full h-full object-contain" />
    </div>
  </div>
</section>

<!-- S4: PearBook — imagen izquierda, texto derecha -->
<section
  bind:this={showcaseB}
  class="py-24 px-6 border-t"
  style="background: var(--color-card); border-color: var(--color-border);"
>
  <div class="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
    <div
      class="showcase-img aspect-square rounded-2xl overflow-hidden order-2 lg:order-1"
      style="opacity:0; background: var(--color-secondary);"
    >
      <img src="/pearbook.png" alt="PearBook" class="w-full h-full object-contain" />
    </div>
    <div class="showcase-text order-1 lg:order-2" style="opacity:0;">
      <p class="text-xs font-medium mb-3 tracking-widest uppercase" style="color: var(--color-muted-foreground);">PearBook</p>
      <h2 class="text-3xl sm:text-4xl font-black mb-5" style="line-height: 1.1;">
        Ultra ligero. Ultra pera.
      </h2>
      <p class="leading-relaxed" style="color: var(--color-muted-foreground);">
        Tan fino que lo perderás encima de la mesa. Tan rápido que encontrarás la excusa para comprarte otro.
      </p>
    </div>
  </div>
</section>

<!-- S5: CTA dark -->
<section
  bind:this={ctaSection}
  class="py-32 px-6 text-center"
  style="background-color: #1d1d1f;"
>
  <p class="cta-child text-xs font-medium mb-4 tracking-widest uppercase" style="opacity:0; color: rgba(255,255,255,0.4);">
    Pear Store
  </p>
  <h2
    class="cta-child font-black mb-6 text-white"
    style="opacity:0; font-size: clamp(2rem, 6vw, 4rem); letter-spacing: -0.04em; line-height: 1.1;"
  >
    ¿Listo para tu próxima pera?
  </h2>
  <p class="cta-child text-base mb-10" style="opacity:0; color: rgba(255,255,255,0.5); line-height: 1.6;">
    Únete a los millones que ya han cambiado cómo comen fruta.<br>O al menos cómo la compran.
  </p>
  <button
    class="cta-child inline-flex items-center justify-center font-medium text-sm px-7 py-3 rounded-md transition-opacity hover:opacity-90 cursor-pointer"
    style="opacity:0; background: #f5f5f5; color: #1d1d1f;"
    onclick={() => push('/login')}
  >
    Empezar ahora
  </button>
  <p class="cta-child text-xs mt-12" style="opacity:0; color: rgba(255,255,255,0.2);">
    Pear · Parodia Conceptual · PW2 2025–26
  </p>
</section>
