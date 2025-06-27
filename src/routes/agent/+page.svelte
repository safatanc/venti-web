<script lang="ts">
	import Icon from '@iconify/svelte';
	import { isDark } from '$lib/stores.js';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	let members = $state(data.members);

	const darkMode = $derived($isDark);

	function toggleTheme() {
		isDark.update((value) => !value);
	}

	function handleSearch(event: KeyboardEvent) {
		const input = event.target as HTMLInputElement;
		const searchQuery = input.value.toLowerCase();

		members = data.members.filter((member) => {
			return member.full_name.toLowerCase().includes(searchQuery);
		});
	}
</script>

<svelte:head>
	<title>Pilih Agent - Venti AI</title>
	<meta name="description" content="Pilih salah satu AI Agent untuk memulai percakapan." />
	<meta name="robots" content="noindex, nofollow" />
</svelte:head>

<div
	class="relative min-h-screen transition-all duration-500 {darkMode
		? 'dark bg-black'
		: 'bg-white'}"
>
	<!-- Gradient overlay -->
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
			<a href="/" class="flex items-center gap-3">
				<img src="/stech_logo_gradient.png" alt="SAFATANC Logo" class="h-8 w-auto" />
				<span class="text-xl font-medium {darkMode ? 'text-white' : 'text-gray-900'}">Venti AI</span
				>
			</a>
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

	<!-- Main Content -->
	<main class="relative z-10 px-6 py-16 sm:py-24">
		<div class="mx-auto max-w-7xl">
			<!-- Header -->
			<div class="text-center">
				<p class="text-primary text-sm font-medium tracking-wider uppercase">JKT48</p>
				<h1
					class="mt-2 text-4xl font-medium tracking-tight sm:text-5xl {darkMode
						? 'text-white'
						: 'text-gray-900'}"
				>
					Pilih AI Agent
				</h1>
				<p
					class="mx-auto mt-6 max-w-2xl text-lg leading-8 {darkMode
						? 'text-gray-400'
						: 'text-gray-600'}"
				>
					Setiap agent memiliki basis pengetahuan dari profil anggota JKT48. Pilih salah satu untuk
					memulai.
				</p>
			</div>

			<!-- Search Bar -->
			<div class="mt-10">
				<input
					type="text"
					placeholder="Cari agent..."
					class="w-full rounded-full border border-gray-300 bg-white/10 px-5 py-2 text-gray-900 outline-none {darkMode
						? 'text-white'
						: 'text-gray-900'}"
					onkeyup={handleSearch}
				/>
			</div>
			<!-- Agent List -->
			{#if data.members?.length > 0}
				<div class="mt-20 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
					{#each members as member (member.id)}
						<a href={`/agent/${member.id}`} class="group block">
							<div
								class="flex h-full flex-col overflow-hidden rounded-2xl border text-left transition-all duration-300 {darkMode
									? 'border-white/10 bg-white/[.05] hover:border-white/20 hover:bg-white/[.08]'
									: 'border-gray-200/80 bg-white hover:border-gray-300 hover:shadow-lg'}"
							>
								{#if member.profile_picture_url}
									<div class="aspect-[3/4] overflow-hidden">
										<img
											src={member.profile_picture_url}
											alt="Foto profil {member.full_name}"
											class="h-full w-full object-cover object-top transition-transform duration-300 group-hover:scale-105"
										/>
									</div>
								{/if}
								<div class="flex flex-1 flex-col p-5">
									<h3 class="text-lg font-semibold {darkMode ? 'text-white' : 'text-gray-900'}">
										{member.full_name || member.name}
									</h3>
									{#if member.birth_date}
										<p class="text-sm {darkMode ? 'text-gray-400' : 'text-gray-600'}">
											{member.birth_place || 'Lokasi tidak diketahui'}, {member.birth_date}
										</p>
									{/if}
									{#if member.introduction_phrase}
										<p
											class="mt-4 flex-1 text-sm italic {darkMode
												? 'text-gray-400'
												: 'text-gray-500'}"
										>
											"{member.introduction_phrase}"
										</p>
									{/if}
								</div>
							</div>
						</a>
					{/each}
				</div>
			{:else}
				<p class="text-center text-gray-500">Tidak ada anggota JKT48 yang ditemukan.</p>
			{/if}
		</div>
	</main>
</div>
