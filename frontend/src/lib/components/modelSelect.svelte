<script lang="ts">
	import { storedModel, availableModels } from '$lib/stores';

	function handleModelChange(event: Event) {
		const select = event.target as HTMLSelectElement;
		storedModel.value = select.value;
	}
</script>

<div class="model-container">
	<div class="setting-item">
		<label for="model-select">Select Model:</label>
		<select value={storedModel.value} onchange={handleModelChange}>
			{#each availableModels.value as model}
				<option value={model}>{model}</option>
			{/each}
		</select>
	</div>
</div>

<style>
	.model-container {
		color: var(--text-2);
		background: var(--surface-1);
		padding: 1rem;
		border-radius: 6px;
		border: 2px solid var(--border-1);
	}

	.setting-item {
		display: flex;
		align-items: center;
		gap: 1rem;
		margin-top: 0.5rem;
	}

	select {
		padding: 0.5rem;
		border-radius: 4px;
		border: 1px solid hsl(220, 13%, 90%);
	}

	label {
		font-weight: 500;
	}
</style>
