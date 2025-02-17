<script>
	import { storedModel, availableModels } from '$lib/stores';

	function handleModelChange(event) {
		const select = event.target;
		storedModel.value = select.value;
	}
</script>

<div class="primary">
	<div class="logo-container">
		<a href="/"><img src="./header1.svg" alt="feddi /guide" class="logo" /></a>
	</div>
	<div class="model-container">
		<div class="setting-item">
			<label for="model-select">model:</label>
			<select
				class="model-select"
				id="model-select"
				bind:value={storedModel.value}
				onchange={handleModelChange}
			>
				{#each availableModels.value as model}
					<option value={model}>{model}</option>
				{/each}
			</select>
		</div>
	</div>
	<nav>
		<ul>
			<li>
				<a href="/">
					<img src="./chat.svg" alt="Chat" />
					<span>chat</span>
				</a>
			</li>
			<li>
				<a href="/documents">
					<img src="./docs.svg" alt="Documents" />
					<span>documents</span>
				</a>
			</li>
			<li>
				<a href="/settings">
					<img src="./settings.svg" alt="Info" />
					<i class="fas fa-cog"></i>
					<span>info</span>
				</a>
			</li>
		</ul>
	</nav>
</div>

<style>
	.primary {
		display: grid;
		grid-template-columns: 1fr auto;
		grid-template-rows: auto auto;
		align-items: center;
		gap: 8px;
		margin-block: 16px;
		width: 100%;
		max-width: 1600px;
		margin-inline: auto;
	}
	.logo-container {
		grid-column: 1 / -1;
		grid-row: 1 / 2;
		display: flex;
		justify-content: center;
		align-items: center;
	}
	.model-container {
		color: var(--text-4);
		border-radius: 6px;
		grid-column: 2 / 3;
		grid-row: 1 / 2;
		justify-self: end;
	}
	.model-select {
		width: 175px;
	}
	nav {
		grid-column: 1 / -1;
		grid-row: 2 / 3;
		justify-self: center;
	}
	nav ul {
		list-style: none;
		padding: 0;
		display: flex;
		gap: 1rem;
	}
	nav a {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.75rem 1rem;
		text-decoration: none;
		color: var(--accent-2);
		border-radius: 8px;
		transition: background-color 0.25s ease-in-out;
	}
	nav a:hover {
		background-color: var(--surface-2);
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
