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
    if (heroEyebrow) animate(heroEyebrow, { opacity: [0, 1], y: [20, 0] }, { duration: 0.5 });
    if (heroHeadline) animate(heroHeadline, { opacity: [0, 1], y: [30, 0] }, { duration: 0.6, delay: 0.1 });
    if (heroSub) animate(heroSub, { opacity: [0, 1], y: [20, 0] }, { duration: 0.5, delay: 0.25 });
    if (heroButtons) animate(heroButtons, { opacity: [0, 1], y: [20, 0] }, { duration: 0.5, delay: 0.4 });

    if (featuresSection) {
      inView(featuresSection, () => {
        const cols = featuresSection!.querySelectorAll('.feature-col');
        animate(cols, { opacity: [0, 1], y: [30, 0] }, { delay: stagger(0.12), duration: 0.5 });
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
        animate(children, { opacity: [0, 1], y: [30, 0] }, { delay: stagger(0.1), duration: 0.5 });
      });
    }
  });
</script>

<!-- S1: Hero -->
<section
  class="min-h-screen flex flex-col items-center justify-center text-center px-6"
  style="background-color: var(--color-background);"
>
  <p
    bind:this={heroEyebrow}
    class="text-xs font-medium mb-6 tracking-widest uppercase"
    style="opacity:0; color: var(--color-muted-foreground);"
  >
    Nuevo · Primavera 2026
  </p>

  <h1
    bind:this={heroHeadline}
    class="font-black mb-6 max-w-4xl"
    style="opacity:0; font-size: clamp(3rem, 8vw, 6rem); letter-spacing: -0.04em; line-height: 1.05; color: var(--color-foreground);"
  >
    El futuro de la pera.
  </h1>

  <p
    bind:this={heroSub}
    class="text-lg mb-10 max-w-md"
    style="opacity:0; color: var(--color-muted-foreground); line-height: 1.6;"
  >
    Pear. Redefiniendo lo que significa morder una pera desde 2026.
  </p>

  <div bind:this={heroButtons} class="flex flex-wrap gap-3 justify-center" style="opacity:0;">
    <button
      class="inline-flex items-center justify-center font-medium text-sm px-6 py-2.5 rounded-md transition-opacity hover:opacity-90 cursor-pointer"
      style="background: var(--color-primary); color: var(--color-primary-foreground);"
      onclick={() => push('/products')}
    >
      Descubrir
    </button>
    <button
      class="inline-flex items-center justify-center font-medium text-sm px-6 py-2.5 rounded-md border transition-colors hover:bg-accent cursor-pointer"
      style="background: transparent; color: var(--color-foreground); border-color: var(--color-border);"
      onclick={() => push('/login')}
    >
      Iniciar sesión
    </button>
  </div>
</section>

<!-- S2: 3 Features -->
<section
  bind:this={featuresSection}
  class="py-24 px-6 border-t"
  style="background: var(--color-card); border-color: var(--color-border);"
>
  <div class="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
    <div class="feature-col" style="opacity:0;">
      <span class="block font-black mb-5 select-none" style="font-size: 2.5rem; line-height: 1; color: var(--color-border);">01</span>
      <h3 class="text-lg font-black mb-3">Diseño puro</h3>
      <p class="text-sm leading-relaxed" style="color: var(--color-muted-foreground);">
        Cada curva, cada detalle, pensado para que tu mano lo reconozca antes que tu mente.
      </p>
    </div>
    <div class="feature-col" style="opacity:0;">
      <span class="block font-black mb-5 select-none" style="font-size: 2.5rem; line-height: 1; color: var(--color-border);">02</span>
      <h3 class="text-lg font-black mb-3">Velocidad extrema</h3>
      <p class="text-sm leading-relaxed" style="color: var(--color-muted-foreground);">
        El chip Pear A1 procesa 47 mordiscos por segundo. Nunca habías comido tan rápido.
      </p>
    </div>
    <div class="feature-col" style="opacity:0;">
      <span class="block font-black mb-5 select-none" style="font-size: 2.5rem; line-height: 1; color: var(--color-border);">03</span>
      <h3 class="text-lg font-black mb-3">Privacidad total</h3>
      <p class="text-sm leading-relaxed" style="color: var(--color-muted-foreground);">
        Tus datos de masticación son tuyos. Fin del comunicado.
      </p>
    </div>
  </div>
</section>

<!-- S3: Showcase A — texto izquierda, forma derecha -->
<section
  bind:this={showcaseA}
  class="py-24 px-6"
  style="background-color: var(--color-background);"
>
  <div class="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
    <div class="showcase-text" style="opacity:0;">
      <p class="text-xs font-medium mb-3 tracking-widest uppercase" style="color: var(--color-muted-foreground);">Diseño</p>
      <h2 class="text-3xl sm:text-4xl font-black mb-5" style="line-height: 1.1;">
        Una forma que cambia todo.
      </h2>
      <p class="leading-relaxed" style="color: var(--color-muted-foreground);">
        Inspirado en la naturaleza. Perfeccionado por ingenieros que claramente tenían demasiado tiempo libre.
      </p>
    </div>
    <div
      class="showcase-img aspect-square rounded-2xl flex items-center justify-center overflow-hidden"
      style="opacity:0; background: var(--color-secondary);"
    >
      <span
        class="font-black select-none"
        style="font-size: clamp(6rem, 15vw, 10rem); line-height: 1; color: var(--color-border);"
      >P</span>
    </div>
  </div>
</section>

<!-- S4: Showcase B — forma izquierda, texto derecha -->
<section
  bind:this={showcaseB}
  class="py-24 px-6 border-t"
  style="background: var(--color-card); border-color: var(--color-border);"
>
  <div class="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
    <div
      class="showcase-img aspect-square rounded-2xl flex items-center justify-center overflow-hidden order-2 lg:order-1"
      style="opacity:0; background: var(--color-accent);"
    >
      <span
        class="font-black select-none"
        style="font-size: clamp(6rem, 15vw, 10rem); line-height: 1; color: var(--color-border);"
      >∞</span>
    </div>
    <div class="showcase-text order-1 lg:order-2" style="opacity:0;">
      <p class="text-xs font-medium mb-3 tracking-widest uppercase" style="color: var(--color-muted-foreground);">Rendimiento</p>
      <h2 class="text-3xl sm:text-4xl font-black mb-5" style="line-height: 1.1;">
        Fluye. Sin fricciones.
      </h2>
      <p class="leading-relaxed" style="color: var(--color-muted-foreground);">
        La experiencia Pear es tan suave que olvidarás que estás comiendo fruta. Hasta que recuerdes el precio.
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
