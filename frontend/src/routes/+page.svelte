<script lang="ts">
	import { availableModels, documentStore } from '$lib/stores';
	import ModelSelect from '$lib/components/modelSelect.svelte';
	import Chat from '$lib/components/chat.svelte';
	import DocumentManager from '$lib/components/documentManager.svelte';

	let { data } = $props();
	const { health, listDocuments } = data;

	if (health?.models_loaded) {
		availableModels.value = health.models_loaded;
	}

	$effect(() => {
		if (listDocuments) {
			documentStore.value = listDocuments;
		}
	});
</script>

<div class="options-grid">
	<div>
		<h1 class="title">Meet Feddi</h1>
		<p>your /guide for FDA-related questions.</p>
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
	<DocumentManager listDocuments={documentStore.value} />
</div>

<style>
	.documents-section {
		margin-block: 3rem;
	}

	.options-grid {
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
