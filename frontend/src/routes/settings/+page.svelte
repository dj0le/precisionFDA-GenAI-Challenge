<script lang="ts">
	import { storedModel, availableModels } from '$lib/stores';
	import MdiGithub from '~icons/mdi/github';
	import MdiCardsHeart from '~icons/mdi/cards-heart';

	let { data } = $props();
	const { health } = data;

	// Update availableModels
	if (health?.models_loaded) {
		availableModels.value = health.models_loaded;
	}
</script>

{#if health}
	<div>
		<p>API Version: {health.api_version}</p>
		<h2 class="title">System Status:</h2>
		<div class="status">
			{health.status}
			<MdiCardsHeart style="font-size: 2em; color: var(--success)" />
		</div>

		<MdiGithub style="font-size: 2em; color: var(--accent-1)" />

		<p>Current Model: {storedModel.value}</p>
		<h3>Available Models:</h3>
		<div class="model-list">
			{#each health.models_loaded as model}
				<div class="model-card">{model}</div>
			{/each}
		</div>
	</div>
{/if}

<style>
	.status {
		display: flex;
		align-items: center;
		justify-content: center;
		text-align: center;
		gap: 8px;
	}
	.model-list {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 16px;
	}
	.model-card {
		border: 1px solid var(--border-1);
		border-radius: 6px;
		background-color: var(--surface-2);
		padding: 24px;
		display: grid;
		place-items: center;
	}
</style>
