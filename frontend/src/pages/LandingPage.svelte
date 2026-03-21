<script lang="ts">
  import { onMount } from 'svelte';
  import { push } from 'svelte-spa-router';
  import { animate, inView, stagger } from 'motion';

  let heroEyebrow: HTMLElement | undefined = $state();
  let heroHeadline: HTMLElement | undefined = $state();
  let heroSub: HTMLElement | undefined = $state();
  let heroButtons: HTMLElement | undefined = $state();
  let featuresSection: HTMLElement | undefined = $state();
  let showcaseA: HTMLElement | undefined = $state();
  let showcaseB: HTMLElement | undefined = $state();
  let ctaSection: HTMLElement | undefined = $state();

  onMount(() => {
    // Hero sequence
    if (heroEyebrow) animate(heroEyebrow, { opacity: [0, 1], y: [20, 0] }, { duration: 0.5 });
    if (heroHeadline) animate(heroHeadline, { opacity: [0, 1], y: [30, 0] }, { duration: 0.6, delay: 0.1 });
    if (heroSub) animate(heroSub, { opacity: [0, 1], y: [20, 0] }, { duration: 0.5, delay: 0.25 });
    if (heroButtons) animate(heroButtons, { opacity: [0, 1], y: [20, 0] }, { duration: 0.5, delay: 0.4 });

    // Features stagger
    if (featuresSection) {
      inView(featuresSection, () => {
        const cols = featuresSection!.querySelectorAll('.feature-col');
        animate(cols, { opacity: [0, 1], y: [30, 0] }, { delay: stagger(0.12), duration: 0.5 });
      });
    }

    // Showcase A: text from left, image from right
    if (showcaseA) {
      inView(showcaseA, () => {
        const textEl = showcaseA!.querySelector('.showcase-text');
        const imgEl = showcaseA!.querySelector('.showcase-img');
        if (textEl) animate(textEl, { opacity: [0, 1], x: [-50, 0] }, { duration: 0.6 });
        if (imgEl) animate(imgEl, { opacity: [0, 1], x: [50, 0] }, { duration: 0.6, delay: 0.1 });
      });
    }

    // Showcase B: image from left, text from right
    if (showcaseB) {
      inView(showcaseB, () => {
        const imgEl = showcaseB!.querySelector('.showcase-img');
        const textEl = showcaseB!.querySelector('.showcase-text');
        if (imgEl) animate(imgEl, { opacity: [0, 1], x: [-50, 0] }, { duration: 0.6 });
        if (textEl) animate(textEl, { opacity: [0, 1], x: [50, 0] }, { duration: 0.6, delay: 0.1 });
      });
    }

    // CTA section
    if (ctaSection) {
      inView(ctaSection, () => {
        const children = ctaSection!.querySelectorAll('.cta-child');
        animate(children, { opacity: [0, 1], y: [30, 0] }, { delay: stagger(0.1), duration: 0.5 });
      });
    }
  });
</script>

<!-- S1: Hero -->
<section
  class="min-h-screen flex flex-col items-center justify-center text-center px-6"
  style="background-color: #f5f5f7;"
>
  <p
    bind:this={heroEyebrow}
    class="text-sm font-medium mb-6"
    style="opacity:0; color: var(--color-apple-blue);"
  >
    Nuevo · Primavera 2026
  </p>

  <h1
    bind:this={heroHeadline}
    class="font-semibold mb-6 max-w-4xl"
    style="opacity:0; font-size: clamp(3rem, 8vw, 6rem); letter-spacing: -0.04em; line-height: 1.05; color: var(--color-foreground);"
  >
    El futuro de la pera.
  </h1>

  <p
    bind:this={heroSub}
    class="text-xl mb-10 max-w-xl"
    style="opacity:0; color: var(--color-muted-foreground); line-height: 1.5;"
  >
    iPear. Redefiniendo lo que significa morder una pera desde 2026.
  </p>

  <div bind:this={heroButtons} class="flex flex-wrap gap-3 justify-center" style="opacity:0;">
    <button class="btn-apple text-base px-6 py-3" onclick={() => push('/products')}>
      Descubrir →
    </button>
    <button class="btn-apple-outline text-base px-6 py-3" onclick={() => push('/login')}>
      Ver más
    </button>
  </div>
</section>

<!-- S2: 3 Features -->
<section
  bind:this={featuresSection}
  class="py-24 px-6"
  style="background: white;"
>
  <div class="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
    <div class="feature-col" style="opacity:0;">
      <div class="text-4xl mb-5">✦</div>
      <h3 class="text-xl font-semibold mb-3" style="letter-spacing: -0.02em;">Diseño puro</h3>
      <p class="text-sm leading-relaxed" style="color: var(--color-muted-foreground);">
        Cada curva, cada detalle, pensado para que tu mano lo reconozca antes que tu mente.
      </p>
    </div>
    <div class="feature-col" style="opacity:0;">
      <div class="text-4xl mb-5">⚡</div>
      <h3 class="text-xl font-semibold mb-3" style="letter-spacing: -0.02em;">Velocidad extrema</h3>
      <p class="text-sm leading-relaxed" style="color: var(--color-muted-foreground);">
        El chip iPear A1 procesa 47 mordiscos por segundo. Nunca habías comido tan rápido.
      </p>
    </div>
    <div class="feature-col" style="opacity:0;">
      <div class="text-4xl mb-5">🔒</div>
      <h3 class="text-xl font-semibold mb-3" style="letter-spacing: -0.02em;">Privacidad total</h3>
      <p class="text-sm leading-relaxed" style="color: var(--color-muted-foreground);">
        Tus datos de masticación son tuyos. Fin del comunicado.
      </p>
    </div>
  </div>
</section>

<!-- S3: Showcase A — texto izquierda, imagen derecha -->
<section
  bind:this={showcaseA}
  class="py-24 px-6"
  style="background-color: #f5f5f7;"
>
  <div class="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
    <div class="showcase-text" style="opacity:0;">
      <p class="text-sm font-medium mb-3" style="color: var(--color-apple-blue);">Diseño</p>
      <h2 class="text-3xl sm:text-4xl font-semibold mb-5" style="letter-spacing: -0.03em; line-height: 1.1;">
        Una forma que cambia todo.
      </h2>
      <p class="leading-relaxed" style="color: var(--color-muted-foreground);">
        Inspirado en la naturaleza. Perfeccionado por ingenieros que claramente tenían demasiado tiempo libre.
      </p>
    </div>
    <div
      class="showcase-img aspect-square rounded-3xl flex items-center justify-center text-8xl"
      style="opacity:0; background: linear-gradient(135deg, #e8f4fd 0%, #bee3f8 100%);"
    >
      🍐
    </div>
  </div>
</section>

<!-- S3: Showcase B — imagen izquierda, texto derecha -->
<section
  bind:this={showcaseB}
  class="py-24 px-6"
  style="background: white;"
>
  <div class="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
    <div
      class="showcase-img aspect-square rounded-3xl flex items-center justify-center text-8xl order-2 lg:order-1"
      style="opacity:0; background: linear-gradient(135deg, #e8fdf0 0%, #c6f6d5 100%);"
    >
      🌊
    </div>
    <div class="showcase-text order-1 lg:order-2" style="opacity:0;">
      <p class="text-sm font-medium mb-3" style="color: var(--color-apple-blue);">Rendimiento</p>
      <h2 class="text-3xl sm:text-4xl font-semibold mb-5" style="letter-spacing: -0.03em; line-height: 1.1;">
        Fluye. Sin fricciones.
      </h2>
      <p class="leading-relaxed" style="color: var(--color-muted-foreground);">
        La experiencia iPear es tan suave que olvidarás que estás comiendo fruta. Hasta que recuerdes el precio.
      </p>
    </div>
  </div>
</section>

<!-- S4: CTA dark -->
<section
  bind:this={ctaSection}
  class="py-32 px-6 text-center"
  style="background-color: #1d1d1f;"
>
  <p class="cta-child text-sm font-medium mb-4" style="opacity:0; color: rgba(255,255,255,0.5);">
    iPear Store
  </p>
  <h2
    class="cta-child text-3xl sm:text-5xl font-semibold mb-6 text-white"
    style="opacity:0; letter-spacing: -0.04em; line-height: 1.1;"
  >
    ¿Listo para tu próxima pera?
  </h2>
  <p class="cta-child text-lg mb-10" style="opacity:0; color: rgba(255,255,255,0.6);">
    Únete a los millones que ya han cambiado cómo comen fruta. O al menos cómo la compran.
  </p>
  <button
    class="cta-child btn-apple text-base px-8 py-3"
    style="opacity:0;"
    onclick={() => push('/login')}
  >
    Empezar ahora
  </button>
  <p class="cta-child text-xs mt-12" style="opacity:0; color: rgba(255,255,255,0.3);">
    iPear · Parodia Conceptual · PW2 2025–26
  </p>
</section>
