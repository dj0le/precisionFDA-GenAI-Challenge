<script lang="ts">
	import { storedModel, availableModels } from '$lib/stores';

	import MdiCardsHeart from '~icons/mdi/cards-heart';

	let { data } = $props();
	const { health } = data;

	// Update availableModels
	if (health?.models_loaded) {
		availableModels.value = health.models_loaded;
	}
</script>

{#if health}
	<div class="settings-container">
		<div class="status-section">
			<div>
				<div class="status">
					<h2 class="title">System Status:</h2>
					{health.status}
					<MdiCardsHeart width="2em" height="2em" color="var(--success)" />
				</div>
				<p>API Version: {health.api_version}</p>
			</div>
			<div>
				<p>Current Model: {storedModel.value}</p>
			</div>
		</div>
		<div class="model-section">
			<h3 class="title">Available Models:</h3>
			<div class="model-list">
				{#each health.models_loaded as model}
					<div class="model-card">{model}</div>
				{/each}
			</div>
		</div>
	</div>
{/if}

<style>
	.status-section {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 16px;
		margin-bottom: 24px;
	}
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

	@media (min-width: 864px) {
		.model-list {
			grid-template-columns: repeat(4, minmax(200px, 1fr));
		}
	}
</style>
