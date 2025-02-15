<script lang="ts">
	import type { ToastType } from '$lib/types';
	import { fade } from 'svelte/transition';

	const {
		message = '',
		type = 'info',
		duration = 3000
	} = $props<{
		message?: string;
		type?: ToastType;
		duration?: number;
	}>();

	let showToast = $state(false);
	let timeoutId: number | undefined;

	let iconPath = $derived(`./${type}.svg`);

	$effect(() => {
		if (message) {
			showToast = true;

			timeoutId = setTimeout(() => {
				showToast = false;
			}, duration);
		}
		return () => {
			if (timeoutId) {
				clearTimeout(timeoutId);
			}
		};
	});
</script>

{#if showToast}
	<div class="toast {type}" transition:fade={{ duration: 300 }}>
		<div class="toast-icon {type}">
			<img src={iconPath} alt={type} />
		</div>
		<div class="toast-message">{message}</div>
	</div>
{/if}

<style>
	.toast {
		position: fixed;
		top: 32px;
		right: 32px;
		display: grid;
		grid-template-columns: auto 1fr;
		align-items: center;
		border-radius: 6px;
		overflow: hidden;
		margin-bottom: 10px;
	}
	.toast-message {
		padding: 10px 20px;
		background: var(--surface-2);
		word-break: break-word;
	}
	.toast-icon {
		padding: 10px;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	.toast.success {
		border: 2px solid var(--success);
	}
	.toast.error {
		border: 2px solid var(--error);
	}
	.toast.info {
		border: 2px solid var(--info);
	}
	.toast.warning {
		border: 2px solid var(--warning);
	}
	.toast-icon.warning {
		background-color: var(--warning);
	}
	.toast-icon.error {
		background-color: var(--error);
	}
	.toast-icon.success {
		background-color: var(--success);
	}
	.toast-icon.info {
		background-color: var(--info);
	}
</style>
