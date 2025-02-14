<script lang="ts">
	import { documentStore } from '$lib/stores';
	import type { Document } from '$lib/types';
	import type { ToastType } from '$lib/types';
	import UploadFile from './uploadFile.svelte';
	import Toast from './toast.svelte';
	import { onMount } from 'svelte';

	interface DisplayDocument extends Document {
		displayIndex: number;
	}

	let { listDocuments } = $props<{
		listDocuments: Document[];
	}>();

	// Initialize store with listDocuments when it changes
	$effect(() => {
		if (listDocuments) {
			documentStore.value = listDocuments;
		}
	});

	let uploadError = $state('');
	let sortField = $state('upload_timestamp');
	let sortDirection = $state('desc');
	let searchQuery = $state('');
	let toastMessage = $state('');
	let toastType = $state<ToastType>('info');

	let displayDocuments: DisplayDocument[] = $derived(
		documentStore.value
			.filter((doc) => doc.filename.toLowerCase().includes(searchQuery.toLowerCase()))
			.sort((a, b) => {
				let comparison = 0;
				switch (sortField) {
					case 'filename':
						comparison = a.filename.localeCompare(b.filename);
						break;
					case 'upload_timestamp':
						comparison =
							new Date(a.upload_timestamp).getTime() - new Date(b.upload_timestamp).getTime();
						break;
				}
				return sortDirection === 'asc' ? comparison : -comparison;
			})
			.map((doc, index) => ({
				...doc,
				displayIndex: index + 1
			}))
	);

	function handleSort(field: string) {
		if (sortField === field) {
			sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
		} else {
			sortField = field;
			sortDirection = 'asc';
		}
	}

	async function handleFileUpload(files: File[]) {
		console.log('Files uploaded:', files);

		const uploadedFileNames = files.map((file) => file.name).join(', ');

		for (const file of files) {
			uploadError = '';

			try {
				const formData = new FormData();
				formData.append('file', file);

				const response = await fetch('http://localhost:8000/upload-doc', {
					method: 'POST',
					body: formData
				});

				if (!response.ok) {
					const errorData = await response.json();
					let errorMessage = errorData.detail || 'Upload failed';

					if (errorData.detail?.includes('File already exists with ID:')) {
						errorMessage = 'This document has already been uploaded.';
					}

					toastMessage = `Error uploading ${file.name}: ${errorMessage}`;
					toastType = 'error';
					setTimeout(() => {
						toastMessage = '';
					}, 5000); // 5 seconds
					continue;
				}

				if (response.ok) {
					const newDoc = await response.json();
					const completeDoc = {
						file_id: newDoc.file_id,
						filename: file.name,
						upload_timestamp: new Date().toISOString(),
						...newDoc
					};
					documentStore.value = [...documentStore.value, completeDoc];
				}
			} catch (error) {
				console.error('Upload error:', error);
				toastMessage = `Error uploading ${file.name}: ${error instanceof Error ? error.message : 'Upload failed'}`;
				toastType = 'error';
				setTimeout(() => {
					toastMessage = '';
				}, 5000);
			}
		}

		toastMessage = `Uploaded: ${uploadedFileNames}`;
		toastType = 'success';
		setTimeout(() => {
			toastMessage = '';
		}, 3000); // 3 seconds
	}

	async function handleDelete(fileId: string) {
		try {
			const response = await fetch('http://localhost:8000/delete-doc', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ file_id: fileId })
			});

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.detail || 'Delete failed');
			}

			if (response.ok) {
				documentStore.value = documentStore.value.filter((doc) => doc.file_id !== fileId);
			}
		} catch (error) {
			console.error('Delete error:', error);
			alert(error instanceof Error ? error.message : 'Delete failed');
		}
	}
	onMount(() => {
		console.log('listDocuments: ', $inspect(listDocuments));
	});

	function formatFilename(filename: string): string {
		const nameWithoutExtension = filename.endsWith('.pdf') ? filename.slice(0, -4) : filename;

		if (nameWithoutExtension.length > 25) {
			return nameWithoutExtension.slice(0, 25) + '...';
		}

		return nameWithoutExtension;
	}
</script>

<Toast message={toastMessage} type={toastType} />

<div class="document-manager">
	<div class="documents-section">
		<div class="column-left">
			<div>
				<h2 class="title">Available Documents</h2>
			</div>
			<div class="controls">
				<input
					type="search"
					placeholder="Search documents..."
					bind:value={searchQuery}
					class="search-input"
				/>
			</div>
		</div>
		<div class="upload-section">
			<UploadFile onUpload={handleFileUpload} />
		</div>
	</div>

	{#if uploadError}
		<div class="error-message" role="alert">
			{uploadError}
		</div>
	{/if}

	{#if documentStore.value.length > 0}
		<div class="documents-grid">
			<div class="documents-header">
				<div class="documents-cell">Number</div>
				<div class="documents-cell">
					<button
						type="button"
						class="sort-button"
						onclick={() => handleSort('filename')}
						onkeydown={(e) => e.key === 'Enter' && handleSort('filename')}
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
						onclick={() => handleSort('upload_timestamp')}
						onkeydown={(e) => e.key === 'Enter' && handleSort('upload_timestamp')}
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
						<button class="delete button" onclick={() => handleDelete(doc.file_id)}>
							Delete
						</button>
					</div>
				</div>
			{/each}
		</div>
	{:else}
		<p>No documents available</p>
	{/if}
</div>

<style>
	.controls {
		margin-bottom: 1rem;
	}
	.search-input {
		padding: 0.5rem;
		border: 1px solid var(--border-1);
		border-radius: 4px;
		width: 100%;
		max-width: 300px;
	}
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
	.documents-section {
		display: grid;
		grid-template-columns: 1fr 1fr;

		align-items: center;
	}
	.column-left {
		display: grid;
		grid-template-rows: 1fr 1fr;
		align-items: start;
		gap: 16px;
	}
	.document-manager {
		margin-bottom: 1rem;
	}

	.upload-section {
		justify-self: end;
	}
	.error-message {
		color: var(--error);
		background-color: var(#f7d4d7);
		border: 1px solid var(#ed9ba4);
		border-radius: 6px;
		padding: 0.75rem 1.25rem;
		margin-top: 0.5rem;
	}
	.delete {
		background-color: var(--error);
		border: none;
	}
	.delete:hover {
		background-color: #c42126;
	}
</style>
