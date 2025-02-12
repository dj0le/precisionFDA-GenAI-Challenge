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
		<select>
			value={storedModel.value} onchange={handleModelChange}>
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
		border-radius: 6px;
		padding: 1rem;
	}

	.setting-item {
		display: flex;
		align-items: center;
		gap: 1rem;
		margin-top: 0.5rem;
	}

	select {
		padding: 8px;
		border-radius: 6px;
	}

	.setting-item select {
		border: 1px solid var(--border-1);
		background-color: var(--surface-1);
		padding: 8px 16px;
	}

	.setting-item select:focus {
		border-color: var(--accent-2);
		outline: none;
	}
</style>
