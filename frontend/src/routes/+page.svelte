<script lang="ts">
	import { availableModels } from '$lib/stores';
	import ModelSelect from '$lib/components/modelSelect.svelte';
	import Chat from '$lib/components/chat.svelte';

	let { data } = $props();
	const { health } = data;

	if (health?.models_loaded) {
		availableModels.value = health.models_loaded;
	}
</script>

<div class="container">
	{#if health}
		<div class="model-section">
			<ModelSelect />
		</div>
	{/if}

	<div class="chat-section">
		<Chat />
	</div>
</div>

<style>
	.container {
		border: 1px solid var(--border-1);
		border-radius: 6px;
		padding: var(--padding);
	}
	.chat-section {
		margin-block: 2rem;
		border-radius: 6px;
		padding: var(--padding);
	}
</style>
