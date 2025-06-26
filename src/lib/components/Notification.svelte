<script lang="ts">
	import { appState, removeNotification } from '../stores.js';
	import { fly } from 'svelte/transition';
	import Icon from '@iconify/svelte';

	$: notifications = $appState.notifications;

	function getIcon(type: string) {
		switch (type) {
			case 'success':
				return 'tabler:check-circle';
			case 'error':
				return 'tabler:x-circle';
			case 'warning':
				return 'tabler:alert-triangle';
			case 'info':
				return 'tabler:info-circle';
			default:
				return 'tabler:info-circle';
		}
	}

	function getColorClass(type: string) {
		switch (type) {
			case 'success':
				return 'border-green-400 text-green-800 dark:text-green-200';
			case 'error':
				return 'border-red-400 text-red-800 dark:text-red-200';
			case 'warning':
				return 'border-yellow-400 text-yellow-800 dark:text-yellow-200';
			case 'info':
				return 'border-blue-400 text-blue-800 dark:text-blue-200';
			default:
				return 'border-gray-400 text-gray-800 dark:text-gray-200';
		}
	}
</script>

<!-- Notification Container -->
<div class="fixed right-4 bottom-4 z-50 max-w-sm space-y-2">
	{#each notifications as notification (notification.id)}
		<div
			class="glass dark:glass-dark rounded-2xl border-l-4 p-4 {getColorClass(
				notification.type
			)} animate-slide-in shadow-lg"
			in:fly={{ x: 300, duration: 300 }}
			out:fly={{ x: 300, duration: 200 }}
		>
			<div class="flex items-center justify-between">
				<div class="flex items-center space-x-3">
					<Icon icon={getIcon(notification.type)} class="h-5 w-5" />
					<p class="text-sm font-medium">{notification.message}</p>
				</div>
				<button
					onclick={() => removeNotification(notification.id)}
					class="ml-4 text-gray-500 transition-colors hover:text-gray-700 dark:hover:text-gray-300"
				>
					<Icon icon="tabler:x" class="h-4 w-4" />
				</button>
			</div>
		</div>
	{/each}
</div>
