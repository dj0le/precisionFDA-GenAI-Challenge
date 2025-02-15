<script lang="ts">
	import { storedModel, availableModels } from '$lib/stores';

	let { data } = $props();
	const { health } = data;

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
