<script lang="ts">
	import { onMount } from 'svelte';
	import Icon from '@iconify/svelte';
	import { isDark } from '$lib/stores.js';

	let mounted = $state(false);
	const darkMode = $derived($isDark);

	function toggleTheme() {
		isDark.update((value) => !value);
	}

	onMount(() => {
		mounted = true;
	});
</script>

<svelte:head>
	<title>Venti AI - Intelligent Assistant SAFATANC GROUP</title>
	<meta name="description" content="Intelligent Assistant SAFATANC GROUP" />

	<!-- Open Graph / Facebook -->
	<meta property="og:type" content="website" />
	<meta property="og:title" content="Venti AI - Intelligent Assistant SAFATANC GROUP" />
	<meta property="og:description" content="Intelligent Assistant SAFATANC GROUP" />
	<meta property="og:site_name" content="PT SAFATANC TECHNOLOGY DIGITAL" />

	<!-- Twitter -->
	<meta name="twitter:card" content="summary" />
	<meta name="twitter:title" content="Venti AI - Intelligent Assistant SAFATANC GROUP" />
	<meta name="twitter:description" content="Intelligent Assistant SAFATANC GROUP" />

	<!-- Additional Meta -->
	<meta
		name="keywords"
		content="Venti AI, SAFATANC GROUP, GetLayar, GSalt, Tipspace, Parkingo, GPrestore, Safatanc Connect, AI Assistant, Digital Solutions"
	/>
	<meta name="author" content="PT SAFATANC TECHNOLOGY DIGITAL" />
	<meta name="robots" content="index, follow" />
	<meta name="language" content="id" />

	<!-- Canonical URL -->
	<link rel="canonical" href="https://venti.safatanc.com" />
</svelte:head>

<div
	class="relative min-h-screen transition-all duration-500 {darkMode
		? 'dark bg-black'
		: 'bg-white'}"
>
	<!-- Subtle gradient overlay -->
	<div class="pointer-events-none absolute inset-0">
		<div
			class="absolute inset-0 bg-gradient-to-br {darkMode
				? 'from-black/70 to-black'
				: 'from-gray-100/70 to-white'}"
		></div>
		<div
			class="from-primary/5 absolute top-0 right-0 h-[800px] w-[800px] bg-gradient-to-b via-transparent to-transparent blur-[120px]"
		></div>
	</div>

	<!-- Navigation -->
	<nav class="relative z-10 border-b {darkMode ? 'border-white/5' : 'border-gray-200/10'}">
		<div class="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
			<div class="flex items-center gap-3">
				<img src="/stech_logo_gradient.png" alt="SAFATANC Logo" class="h-8 w-auto" />
				<span class="text-xl font-medium {darkMode ? 'text-white' : 'text-gray-900'}">Venti AI</span
				>
			</div>
			<div class="flex items-center gap-4">
				<button
					onclick={toggleTheme}
					class="rounded-full p-2 transition-all duration-300 {darkMode
						? 'text-gray-400 hover:bg-white/5'
						: 'text-gray-600 hover:bg-gray-100'}"
				>
					{#if darkMode}
						<Icon icon="tabler:sun" class="h-5 w-5" />
					{:else}
						<Icon icon="tabler:moon" class="h-5 w-5" />
					{/if}
				</button>
				<a
					href="/chat"
					class="bg-primary hover:bg-primary/90 rounded-3xl px-5 py-2 font-medium text-black transition"
				>
					#AskVenti
				</a>
			</div>
		</div>
	</nav>

	<!-- Hero Section -->
	<main class="relative z-10">
		<div class="mx-auto w-full max-w-screen-md px-8 pt-32 text-center">
			<p class="text-primary mb-3 text-sm font-medium tracking-wider uppercase">Venti</p>
			<h1 class="text-6xl leading-tight font-medium {darkMode ? 'text-white' : 'text-gray-900'}">
				Intelligent Ecosystem
				<br />
				<span
					class="from-primary to-primary/80 bg-gradient-to-r bg-clip-text font-bold text-transparent"
				>
					Assistant
				</span>
			</h1>
			<p
				class="mx-auto mt-6 max-w-[600px] text-lg leading-relaxed {darkMode
					? 'text-gray-400'
					: 'text-gray-600'}"
			>
				Intelligent Ecosystem for Safatanc Group
			</p>
			<a
				href="/chat"
				class="bg-primary hover:bg-primary/90 mt-8 inline-flex items-center rounded-3xl px-6 py-2.5 font-medium text-black transition"
			>
				Start #AskVenti
			</a>
		</div>

		<!-- Supported Products -->
		<div class="mx-auto mt-32 max-w-7xl px-6">
			<p
				class="text-center text-xs tracking-wider uppercase {darkMode
					? 'text-gray-600'
					: 'text-gray-500'}"
			>
				Our Supported Products
			</p>
			<div
				class="mt-8 flex flex-wrap items-center justify-center gap-16 opacity-50 grayscale transition duration-300 hover:opacity-100 hover:grayscale-0"
			>
				<img
					src="/stech_logo_gradient.png"
					alt="SAFATANC"
					class="aspect-square h-16 object-contain"
				/>
				<img src="/getlayar.png" alt="GetLayar" class="aspect-square h-16 object-contain" />
				<img src="/GSalt.png" alt="GSalt" class="aspect-square h-16 object-contain" />
				<img src="/tipspace.png" alt="Tipspace" class="aspect-square h-16 object-contain" />
				<img src="/idcardku.png" alt="IDCardku" class="aspect-square h-16 object-contain" />
			</div>
		</div>

		<!-- Company Copyright -->
		<div class="mx-auto max-w-7xl px-6 py-32">
			<p
				class="text-center text-xs tracking-wider uppercase {darkMode
					? 'text-gray-600'
					: 'text-gray-500'}"
			>
				© 2025 Venti AI | PT SAFATANC TECHNOLOGY DIGITAL
			</p>
		</div>
	</main>
</div>
