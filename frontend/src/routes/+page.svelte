<script lang="ts">
	import { storedModel, availableModels } from '$lib/stores';
	import ModelSelect from '$lib/components/modelSelect.svelte';
	import Chat from '$lib/components/chat.svelte';

	let { data } = $props();
	const { health, documents } = data;

	// Update availableModels
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

{#if documents && documents.length > 0}
	<div class="documents-section">
		<h2 class="title">Available Documents</h2>
		<div class="documents-grid">
			<div class="documents-header">
				<div class="documents-cell">File ID</div>
				<div class="documents-cell">Filename</div>
				<div class="documents-cell">Upload Date</div>
			</div>
			{#each documents as doc}
				<div class="documents-row">
					<div class="documents-cell">{doc.file_id}</div>
					<div class="documents-cell">{doc.filename}</div>
					<div class="documents-cell">{new Date(doc.upload_timestamp).toLocaleString()}</div>
				</div>
			{/each}
		</div>
	</div>
{:else}
	<p>No documents available</p>
{/if}

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
