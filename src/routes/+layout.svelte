<script lang="ts">
	import { isDark } from '$lib/stores.js';
	import Notification from '$lib/components/Notification.svelte';
	import Icon from '@iconify/svelte';
	let { children } = $props();
	import '../tailwind.css';

	const darkMode = $derived($isDark);

	function toggleTheme() {
		isDark.update((value) => !value);
	}
</script>

<svelte:head>
	<title>Venti AI - Intelligent Assistant</title>
	<meta
		name="description"
		content="Venti AI - Asisten AI yang cerdas dan ramah untuk SAFATANC GROUP"
	/>
</svelte:head>

<div
	class="font-jakartamin-h-screen transition-all duration-500 {darkMode
		? 'dark bg-black'
		: 'bg-gradient-to-br from-orange-50 via-yellow-50 to-amber-50'}"
>
	<!-- Background Pattern -->
	<div class="pointer-events-none fixed inset-0 opacity-30">
		<div class="absolute inset-0 {darkMode ? 'liquid-gradient-dark' : 'liquid-gradient'}"></div>
		<div
			class="animate-float bg-primary/20 absolute top-20 left-20 h-72 w-72 rounded-full blur-3xl"
		></div>
		<div
			class="animate-float bg-primary/10 absolute right-20 bottom-20 h-96 w-96 rounded-full blur-3xl"
			style="animation-delay: -1s;"
		></div>
		<div
			class="animate-float bg-primary/15 absolute top-1/2 left-1/2 h-64 w-64 rounded-full blur-3xl"
			style="animation-delay: -2s;"
		></div>
	</div>

	<!-- Theme Toggle Button -->
	<button
		onclick={toggleTheme}
		class="fixed bottom-6 left-6 z-40 hidden rounded-full p-3 lg:block {darkMode
			? 'glass-dark text-white'
			: 'glass text-gray-800'} animate-pulse-glow transition-all duration-300 hover:scale-110"
		aria-label="Toggle theme"
	>
		{#if darkMode}
			<Icon icon="tabler:sun" class="h-6 w-6" />
		{:else}
			<Icon icon="tabler:moon" class="h-6 w-6" />
		{/if}
	</button>

	<!-- Notification Component -->
	<Notification />

	<!-- Main Content -->
	<main class="relative z-10">
		{@render children()}
	</main>
</div>
