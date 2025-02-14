<script lang="ts">
	import type { ToastType } from '$lib/types';

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
	<div class="toast {type}">
		{message}
	</div>
{/if}

<style>
	.toast {
		position: fixed;
		top: 40px;
		right: 40px;
		background-color: var(--surface-2);
		color: var(--text-2);
		padding: 12px 24px;
		border-radius: 6px;
		z-index: 1000;
		opacity: 0.95;
		transition: opacity 0.3s ease-in-out;
	}

	.toast.success {
		background-color: var(--success);
	}
	.toast.error {
		background-color: var(--error);
	}
	.toast.info {
		background-color: var(--info);
	}

	.toast.warning {
		background-color: var(--warning);
	}
</style>
