<script lang="ts">
	import { storedModel, availableModels } from '$lib/stores';
	import { invalidateAll } from '$app/navigation';
	import DocumentManager from '$lib/components/documentManager.svelte';

	let { data } = $props();
	const { health, listDocuments } = data;

	// Update availableModels
	if (health?.models_loaded) {
		availableModels.value = health.models_loaded;
	}
	async function refreshDocuments() {
		await invalidateAll();
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

<div class="documents-section">
	{#if listDocuments}
		<DocumentManager {listDocuments} {refreshDocuments} />
	{/if}
</div>

<style>
	.documents-section {
		margin-block: 2rem;
	}
</style>
