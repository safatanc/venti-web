import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// Theme store
export const isDark = writable(false);

// Initialize theme from system preference or localStorage
if (browser) {
	const stored = localStorage.getItem('venti-theme');
	const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

	if (stored) {
		isDark.set(stored === 'dark');
	} else {
		isDark.set(prefersDark);
	}

	// Subscribe to changes and save to localStorage
	isDark.subscribe((value) => {
		if (browser) {
			localStorage.setItem('venti-theme', value ? 'dark' : 'light');
			document.documentElement.classList.toggle('dark', value);
		}
	});
}

// Chat connection store
export const chatConnection = writable({
	isConnected: false,
	reconnectAttempts: 0,
	lastConnected: null as Date | null
});

// App state store
export const appState = writable({
	isLoading: false,
	notifications: [] as Array<{
		id: string;
		type: 'success' | 'error' | 'warning' | 'info';
		message: string;
		timeout?: number;
	}>
});

// Notification helpers
export function addNotification(
	type: 'success' | 'error' | 'warning' | 'info',
	message: string,
	timeout = 5000
) {
	const id = Date.now().toString();
	appState.update((state) => ({
		...state,
		notifications: [...state.notifications, { id, type, message, timeout }]
	}));

	if (timeout > 0) {
		setTimeout(() => {
			removeNotification(id);
		}, timeout);
	}
}

export function removeNotification(id: string) {
	appState.update((state) => ({
		...state,
		notifications: state.notifications.filter((n) => n.id !== id)
	}));
}
