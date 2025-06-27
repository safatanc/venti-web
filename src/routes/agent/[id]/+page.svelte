<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { addNotification, chatConnection, isDark } from '$lib/stores.js';
	import Icon from '@iconify/svelte';
	import { PUBLIC_VENTI_WS_URL } from '$env/static/public';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	type Message = {
		id: string;
		text: string;
		isUser: boolean;
		timestamp: Date;
		model?: string;
		sessionId?: string;
		additional_system_prompt?: string;
	};

	let messages: Message[] = $state([]);
	let inputText = $state('');
	let ws: WebSocket | null = null;
	let isConnected = $state(false);
	let isTyping = $state(false);
	let sessionId = $state('');
	let chatContainer: HTMLDivElement;
	let messageEnd: HTMLDivElement;
	let mounted = $state(false);
	let reconnectAttempts = $state(0);
	const darkMode = $derived($isDark);

	function scrollToBottom() {
		if (!messageEnd) return;
		messageEnd.scrollIntoView({ behavior: 'smooth' });
	}

	function toggleTheme() {
		isDark.update((value) => !value);
	}

	// Watch for changes that should trigger scrolling
	$effect(() => {
		if (messages.length > 0 || isTyping) {
			setTimeout(scrollToBottom, 100);
		}
	});

	// Update global connection state
	$effect(() => {
		chatConnection.update((state) => ({
			...state,
			isConnected,
			reconnectAttempts,
			lastConnected: isConnected ? new Date() : state.lastConnected
		}));
	});

	onMount(() => {
		mounted = true;
		sessionId = generateSessionId();
		connectWebSocket();

		// Add welcome message
		addMessage({
			id: generateId(),
			text: `Halo... Aku ${data.member.name}, Ada apa nih kak?`,
			isUser: false,
			timestamp: new Date()
		});

		return () => {
			if (ws) {
				ws.close();
			}
		};
	});

	function generateSessionId(): string {
		return 'session_' + Date.now() + '_' + Math.random().toString(36).substring(2, 9);
	}

	function generateId(): string {
		return Date.now().toString() + Math.random().toString(36).substring(2, 9);
	}

	function connectWebSocket() {
		if (!browser) return;

		try {
			ws = new WebSocket(PUBLIC_VENTI_WS_URL);

			ws.onopen = () => {
				isConnected = true;
				reconnectAttempts = 0;
				console.log('Connected to Venti AI');
				if (reconnectAttempts > 0) {
					addNotification('success', 'Berhasil terhubung kembali ke Venti AI!');
				}
			};

			ws.onmessage = (event) => {
				try {
					const response = JSON.parse(event.data);

					if (response.error) {
						addMessage({
							id: generateId(),
							text: `Error: ${response.error}`,
							isUser: false,
							timestamp: new Date()
						});
						addNotification('error', `Error dari server: ${response.error}`);
						isTyping = false;
						return;
					}

					if (response.message === '[DONE]') {
						isTyping = false;
						return;
					}

					// Handle streaming response
					if (response.message) {
						updateLastMessage(response.message, response.model, response.session_id);
					}
				} catch (error) {
					console.error('Error parsing message:', error);
					addNotification('error', 'Terjadi kesalahan dalam memproses respons');
					isTyping = false;
				}
			};

			ws.onclose = () => {
				isConnected = false;
				console.log('Disconnected from Venti AI');

				if (reconnectAttempts === 0) {
					addNotification('warning', 'Koneksi terputus, mencoba menyambung kembali...');
				}

				// Try to reconnect after 3 seconds
				setTimeout(() => {
					if (!isConnected && reconnectAttempts < 5) {
						reconnectAttempts++;
						connectWebSocket();
					} else if (reconnectAttempts >= 5) {
						addNotification(
							'error',
							'Gagal menyambung setelah 5 percobaan. Silakan refresh halaman.'
						);
					}
				}, 3000);
			};

			ws.onerror = (error) => {
				console.error('WebSocket error:', error);
				isConnected = false;
				if (reconnectAttempts === 0) {
					addNotification('error', 'Tidak dapat terhubung ke Venti AI');
				}
			};
		} catch (error) {
			console.error('Failed to connect:', error);
			isConnected = false;
			addNotification('error', 'Gagal membuka koneksi WebSocket');
		}
	}

	function addMessage(message: Message) {
		messages = [...messages, message];
		scrollToBottom();
	}

	function updateLastMessage(chunk: string, model?: string, sessionIdFromResponse?: string) {
		if (messages.length === 0 || messages[messages.length - 1].isUser) {
			// Create new message if no AI message exists
			addMessage({
				id: generateId(),
				text: chunk,
				isUser: false,
				timestamp: new Date(),
				model,
				sessionId: sessionIdFromResponse
			});
		} else {
			// Update last AI message
			messages = messages.map((msg, index) => {
				if (index === messages.length - 1 && !msg.isUser) {
					return {
						...msg,
						text: msg.text + chunk,
						model: model || msg.model,
						sessionId: sessionIdFromResponse || msg.sessionId
					};
				}
				return msg;
			});
			scrollToBottom();
		}
	}

	function sendMessage() {
		if (!inputText.trim() || !isConnected || !ws) {
			if (!isConnected) {
				addNotification('warning', 'Tidak terhubung ke server. Tunggu koneksi dipulihkan.');
			}
			return;
		}

		const userMessage: Message = {
			id: generateId(),
			text: inputText.trim(),
			isUser: true,
			timestamp: new Date()
		};

		addMessage(userMessage);

		// Send to Venti AI
		const payload: {
			message: string;
			session_id: string;
			additional_system_prompt?: string;
		} = {
			message: inputText.trim(),
			session_id: sessionId,
			additional_system_prompt: `Sekarang kamu bukan Venti AI, kamu adalah ${data.member.name} dari JKT48, kamu harus berbicara seperti dia. Ini adalah informasi kamu: ${JSON.stringify(data.member)}`
		};

		try {
			ws.send(JSON.stringify(payload));
			inputText = '';
			isTyping = true;
		} catch (error) {
			console.error('Failed to send message:', error);
			addNotification('error', 'Gagal mengirim pesan');
			isTyping = false;
		}
	}

	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			sendMessage();
		}
	}

	function clearChat() {
		messages = [];
		sessionId = generateSessionId();
		addMessage({
			id: generateId(),
			text: 'Chat telah dibersihkan. Ada yang bisa saya bantu?',
			isUser: false,
			timestamp: new Date()
		});
		addNotification('info', 'Chat berhasil dibersihkan');
	}

	function formatTime(date: Date): string {
		return date.toLocaleTimeString('id-ID', {
			hour: '2-digit',
			minute: '2-digit'
		});
	}
</script>

<svelte:head>
	<title>Venti AI - {data.member.name}</title>
	<meta name="description" content={`Agent ${data.member.name}`} />

	<!-- Open Graph / Facebook -->
	<meta property="og:type" content="website" />
	<meta property="og:title" content={`Venti AI - ${data.member.name}`} />
	<meta property="og:description" content={`Agent ${data.member.name}`} />
	<meta property="og:site_name" content="PT SAFATANC TECHNOLOGY DIGITAL" />

	<!-- Twitter -->
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content={`Venti AI - ${data.member.name}`} />
	<meta name="twitter:description" content={`Agent ${data.member.name}`} />
	<meta name="twitter:image" content={data.member.profile_picture_url} />
	<!-- Additional Meta -->
	<meta
		name="keywords"
		content="Venti AI, SAFATANC GROUP, GetLayar, GSalt, Tipspace, Parkingo, GPrestore, Safatanc Connect, AI Assistant, Digital Solutions"
	/>
	<meta name="author" content="PT SAFATANC TECHNOLOGY DIGITAL" />
	<meta name="robots" content="index, follow" />
	<meta name="language" content="id" />

	<!-- Canonical URL -->
	<link rel="canonical" href="https://venti.safatanc.com/chat" />
</svelte:head>

<div
	class="flex h-full min-h-screen flex-col transition-all duration-500 {darkMode
		? 'bg-black'
		: 'bg-white'}"
>
	<!-- Header -->
	<header class="border-b {darkMode ? 'border-white/5' : 'border-gray-200/10'} p-4">
		<div class="mx-auto flex max-w-4xl items-center justify-between">
			<div class="flex items-center space-x-4">
				<a href="/" class="flex items-center gap-3">
					<div
						class="flex h-10 w-10 items-center justify-center overflow-hidden rounded-3xl bg-white"
					>
						<img
							src={data.member.profile_picture_url}
							alt={data.member.name}
							class="h-full w-full object-contain"
						/>
					</div>
					<div>
						<h1 class="text-xl font-medium {darkMode ? 'text-white' : 'text-gray-900'}">
							{data.member.name}
						</h1>
						<div class="flex items-center gap-2 text-xs">
							<div class="h-2 w-2 rounded-full {isConnected ? 'bg-green-400' : 'bg-red-400'}"></div>
							<span class={darkMode ? 'text-gray-400' : 'text-gray-600'}>
								{#if isConnected}
									Terhubung
								{:else if reconnectAttempts > 0}
									Menyambung kembali... ({reconnectAttempts}/5)
								{:else}
									Terputus
								{/if}
							</span>
						</div>
					</div>
				</a>
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
				<button
					onclick={clearChat}
					class="rounded-3xl px-5 py-2 transition-all duration-300 {darkMode
						? 'text-gray-400 hover:bg-white/5'
						: 'text-gray-600 hover:bg-gray-100'}"
					title="Bersihkan Chat"
				>
					<Icon icon="tabler:trash" class="h-5 w-5" />
				</button>
			</div>
		</div>
	</header>

	<!-- Chat Messages -->
	<div class="flex-1 overflow-hidden pb-16">
		<div bind:this={chatContainer} class="h-full space-y-4 overflow-y-auto p-4 pb-16">
			<div class="mx-auto max-w-4xl space-y-4">
				{#each messages as message (message.id)}
					<div class="flex {message.isUser ? 'justify-end' : 'justify-start'}">
						<div class="max-w-xs sm:max-w-md lg:max-w-lg xl:max-w-xl">
							<div class="flex items-end gap-2 {message.isUser ? 'flex-row-reverse' : ''}">
								<!-- Avatar -->
								<div
									class="flex h-8 w-8 flex-shrink-0 items-center justify-center overflow-hidden rounded-3xl {message.isUser
										? 'bg-primary'
										: darkMode
											? 'bg-white/10'
											: 'bg-gray-100'}"
								>
									{#if message.isUser}
										<Icon icon="tabler:user" class="h-4 w-4 text-black" />
									{:else}
										<img
											src={data.member.profile_picture_url}
											alt={data.member.name}
											class="h-full w-full bg-white object-contain"
										/>
									{/if}
								</div>

								<!-- Message Bubble -->
								<div class="flex flex-col gap-1">
									<div
										class="rounded-3xl px-5 py-2 {message.isUser
											? 'bg-primary text-black'
											: darkMode
												? 'bg-white/10 text-white'
												: 'bg-gray-100 text-black'} {message.isUser
											? 'rounded-br-lg'
											: 'rounded-bl-lg'}"
									>
										<p class="text-sm leading-relaxed whitespace-pre-wrap">{message.text}</p>
									</div>
									<div
										class="flex items-center gap-2 text-xs {darkMode
											? 'text-gray-400'
											: 'text-gray-500'} {message.isUser ? 'justify-end' : 'justify-start'}"
									>
										<span>{formatTime(message.timestamp)}</span>
									</div>
								</div>
							</div>
						</div>
					</div>
				{/each}

				<!-- Typing Indicator -->
				{#if isTyping}
					<div class="flex justify-start">
						<div class="max-w-xs sm:max-w-md lg:max-w-lg xl:max-w-xl">
							<div class="flex items-end gap-2">
								<div
									class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-3xl {darkMode
										? 'bg-white/10'
										: 'bg-gray-100'}"
								>
									<Icon icon="tabler:robot" class="text-primary h-4 w-4" />
								</div>
								<div
									class="rounded-3xl rounded-bl-lg {darkMode
										? 'bg-white/10'
										: 'bg-gray-100'} px-5 py-2"
								>
									<div class="flex gap-1">
										<div class="bg-primary h-2 w-2 animate-pulse rounded-full"></div>
										<div
											class="bg-primary h-2 w-2 animate-pulse rounded-full"
											style="animation-delay: 0.1s;"
										></div>
										<div
											class="bg-primary h-2 w-2 animate-pulse rounded-full"
											style="animation-delay: 0.2s;"
										></div>
									</div>
								</div>
							</div>
						</div>
					</div>
				{/if}

				<!-- Invisible element to scroll to -->
				<div bind:this={messageEnd}></div>
			</div>
		</div>
	</div>

	<!-- Input Area -->
	<div
		class="border-t {darkMode
			? 'border-white/5 bg-black'
			: 'border-gray-200/10 bg-white'} fixed right-0 bottom-0 left-0 p-4 pb-16"
	>
		<div class="mx-auto max-w-4xl">
			<div class="flex items-end gap-4">
				<div class="w-full">
					<textarea
						bind:value={inputText}
						onkeydown={handleKeyPress}
						placeholder="Write your message here..."
						class="w-full rounded-3xl border-0 {darkMode
							? 'bg-white/10 text-white placeholder-gray-400'
							: 'bg-gray-100 text-gray-900 placeholder-gray-500'} px-5 py-2 outline-none"
						rows="1"
					></textarea>
				</div>
				<button
					onclick={sendMessage}
					disabled={!inputText.trim() || !isConnected}
					class="bg-primary hover:bg-primary/90 flex h-full items-center justify-center rounded-3xl px-5 py-2 text-black transition disabled:cursor-not-allowed disabled:opacity-50"
					title={isConnected ? 'Kirim pesan' : 'Tidak terhubung'}
				>
					<Icon icon="tabler:send" class="h-6 w-6" />
				</button>
			</div>

			{#if !isConnected}
				<div class="mt-2 text-center">
					<span class="text-sm text-red-400">
						{#if reconnectAttempts > 0}
							<Icon icon="tabler:loader" class="inline h-4 w-4 animate-spin" />
							Mencoba menyambung kembali... ({reconnectAttempts}/5)
						{:else}
							<Icon icon="tabler:wifi-off" class="inline h-4 w-4" />
							Tidak dapat terhubung ke Venti AI
						{/if}
					</span>
				</div>
			{/if}
		</div>
	</div>
</div>
