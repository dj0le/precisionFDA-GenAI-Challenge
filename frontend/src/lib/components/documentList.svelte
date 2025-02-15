<script lang="ts">
	import type { DisplayDocument } from './documentManager.svelte'; // Adjust path
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	let { displayDocuments, sortField, sortDirection } = $props<{
		displayDocuments: DisplayDocument[];
		sortField: string;
		sortDirection: 'asc' | 'desc';
	}>();

	function formatFilename(filename: string): string {
		const nameWithoutExtension = filename.endsWith('.pdf') ? filename.slice(0, -4) : filename;

		if (nameWithoutExtension.length > 25) {
			return nameWithoutExtension.slice(0, 25) + '...';
		}

		return nameWithoutExtension;
	}

	function handleSort(field: string) {
		dispatch('sort', field);
	}

	function handleDelete(fileId: string) {
		dispatch('delete', fileId);
	}
</script>

<div class="documents-grid">
	<div class="documents-header">
		<div class="documents-cell">Number</div>
		<div class="documents-cell">
			<button
				type="button"
				class="sort-button"
				on:click={() => handleSort('filename')}
				on:keydown={(e) => e.key === 'Enter' && handleSort('filename')}
			>
				Filename
				{#if sortField === 'filename'}
					<span class="sort-indicator">
						{sortDirection === 'asc' ? '↑' : '↓'}
					</span>
				{/if}
			</button>
		</div>
		<div class="documents-cell">
			<button
				type="button"
				class="sort-button"
				on:click={() => handleSort('upload_timestamp')}
				on:keydown={(e) => e.key === 'Enter' && handleSort('upload_timestamp')}
			>
				Uploaded
				{#if sortField === 'upload_timestamp'}
					<span class="sort-indicator">
						{sortDirection === 'asc' ? '↑' : '↓'}
					</span>
				{/if}
			</button>
		</div>
		<div class="documents-cell">Actions</div>
	</div>
	{#each displayDocuments as doc}
		<div class="documents-row">
			<div class="documents-cell">{doc.displayIndex}</div>
			<div class="documents-cell">{formatFilename(doc.filename)}</div>
			<div class="documents-cell">{new Date(doc.upload_timestamp).toLocaleString()}</div>
			<div class="documents-cell">
				<button class="delete button" on:click={() => handleDelete(doc.file_id)}> Delete </button>
			</div>
		</div>
	{/each}
</div>

<style>
	.sort-button {
		background: none;
		border: none;
		padding: 0;
		font: inherit;
		color: inherit;
		cursor: pointer;
		width: 100%;
		text-align: left;
		font-weight: 600;
		display: flex;
		align-items: center;
	}

	.sort-button:hover {
		color: var(--accent-1);
	}

	.sort-button:focus {
		outline: 2px solid var(--accent-1);
		outline-offset: 2px;
	}
	.sort-indicator {
		display: inline-block;
		margin-left: 0.5rem;
	}

	.documents-grid {
		display: grid;
		grid-template-columns: 1fr;
		gap: 2px;
		background-color: var(--surface-1);
		border: 1px solid var(--border-1);
		border-radius: 6px;
		overflow: hidden;
	}
	.documents-header {
		display: grid;
		grid-template-columns: 15% 1fr 1fr 15%;
		background-color: var(--surface-2);
		color: var(--text-2);
		font-weight: 600;
		border-bottom: 1px solid var(--border-1);
	}
	.documents-row {
		display: grid;
		grid-template-columns: 15% 1fr 1fr 15%;
		gap: 2px;
		color: var(--text-3);
		background-color: var(--surface-1);
		transition: ease-in-out all 200ms;
	}
	.documents-row:hover {
		color: var(--text-3);
		background-color: var(--surface-3);
	}
	.documents-cell {
		padding: var(--padding);
	}
</style>
