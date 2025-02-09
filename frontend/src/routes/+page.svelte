<script lang="ts">
	import { storedModel, availableModels } from '$lib/stores';
	import ModelSelect from '$lib/components/modelSelect.svelte';

	let { data } = $props();
	const { health, documents } = data;

	// Update availableModels
	if (health?.models_loaded) {
		availableModels.value = health.models_loaded;
	}
</script>

<h1 class="title">Welcome to Feddy /guide</h1>
<p>your personal assistant for FDA-related questions.</p>

{#if health}
	<div class="model-section">
		<ModelSelect />
	</div>
{/if}

{#if documents && documents.length > 0}
	<div class="documents-section">
		<h2 class="title">Available Documents</h2>
		<div class="grid-table">
			<div class="grid-header">
				<div class="cell">File ID</div>
				<div class="cell">Filename</div>
				<div class="cell">Upload Date</div>
			</div>
			{#each documents as doc}
				<div class="row">
					<div class="cell">{doc.file_id}</div>
					<div class="cell">{doc.filename}</div>
					<div class="cell">{new Date(doc.upload_timestamp).toLocaleString()}</div>
				</div>
			{/each}
		</div>
	</div>
{:else}
	<p>No documents available</p>
{/if}

<style>
	.documents-section,
	.model-section {
		margin-block: 3rem;
	}

	.grid-table {
		display: grid;
		grid-template-columns: 1fr;
		gap: 2px;
		background-color: var(--surface-2);
		border-radius: 6px;
		overflow: hidden;
	}

	.grid-header {
		display: grid;
		grid-template-columns: auto 1fr auto;
		gap: 2px;
		color: var(--text-3);
		font-weight: 600;
	}

	.row {
		display: grid;
		grid-template-columns: auto 1fr auto;
		gap: 2px;
		color: var(--text-1);
		background-color: var(--surface-2);
		transition: ease-in-out all 200ms;
	}

	.row:hover {
		color: var(--text-2);
		background-color: var(--surface-3);
	}

	.cell {
		padding: var(--padding);
	}
</style>
