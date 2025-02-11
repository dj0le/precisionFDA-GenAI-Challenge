<script lang="ts">
	import { availableModels } from '$lib/stores';
	import { invalidateAll } from '$app/navigation';
	import ModelSelect from '$lib/components/modelSelect.svelte';
	import Chat from '$lib/components/chat.svelte';
	import DocumentManager from '$lib/components/documentManager.svelte';

	let { data } = $props();
	const { health, listDocuments } = data;

	async function refreshDocuments() {
		console.log('Starting refresh');
		await invalidateAll();
		console.log('Finished refresh');
	}

	$effect(() => {
		console.log('listDocuments changed:', listDocuments);
	});

	if (health?.models_loaded) {
		availableModels.value = health.models_loaded;
	}
</script>

<div class="hero-grid">
	<div>
		<h1 class="title">Welcome to Feddy /guide</h1>
		<p>your personal assistant for FDA-related questions.</p>
	</div>
	{#if health}
		<div class="model-section">
			<ModelSelect />
		</div>
	{/if}
</div>

<div class="chat-section">
	<Chat />
</div>

<div class="documents-section">
	{#if listDocuments}
		<DocumentManager {listDocuments} {refreshDocuments} />
	{/if}
</div>

<style>
	.documents-section {
		margin-block: 3rem;
	}

	.hero-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
	}

	.model-section {
		margin-block: 2rem;
		justify-self: end;
	}

	.chat-section {
		margin-block: 2rem;
		border: 1px solid var(--border-1);
		border-radius: 6px;
		padding: var(--padding);
	}
</style>
