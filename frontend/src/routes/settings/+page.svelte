<script lang="ts">
	import { storedModel, availableModels } from '$lib/stores';

	let { data } = $props();
	const { health, documents } = data;

	// Update availableModels
	if (health?.models_loaded) {
		availableModels.value = health.models_loaded;
	}
</script>

{#if health}
	<div>
		<h2 class="title">System Status</h2>
		<p>Status: {health.status}</p>
		<p>API Version: {health.api_version}</p>
		<p>Current Model: {storedModel.value}</p>
		<p>Models Loaded:</p>
		<ul>
			{#each health.models_loaded as model}
				<li>{model}</li>
			{/each}
		</ul>
	</div>
{/if}

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
		margin-block: 2rem;
	}
</style>
