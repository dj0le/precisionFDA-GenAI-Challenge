<script lang="ts">
	import { documentStore } from '$lib/stores';
	import type { Document } from '$lib/types';

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

	let fileInput: HTMLInputElement;
	let uploadProgress = $state(0);
	let isUploading = $state(false);
	let uploadError = $state('');

	// Add sorting and filtering state
	let sortField = $state('upload_timestamp');
	let sortDirection = $state('desc');
	let searchQuery = $state('');

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

	async function handleFileUpload(event: Event) {
		const input = event.target as HTMLInputElement;
		if (!input.files?.length) return;

		const file = input.files[0];
		isUploading = true;
		uploadProgress = 0;
		uploadError = '';

		try {
			// Create promise to handle XHR upload
			const uploadFile = new Promise<any>((resolve, reject) => {
				const xhr = new XMLHttpRequest();
				const formData = new FormData();
				formData.append('file', file);

				xhr.upload.addEventListener('progress', (event) => {
					if (event.lengthComputable) {
						uploadProgress = Math.round((event.loaded / event.total) * 100);
					}
				});

				xhr.addEventListener('load', () => {
					if (xhr.status >= 200 && xhr.status < 300) {
						resolve(JSON.parse(xhr.response));
					} else {
						reject(new Error('Upload failed'));
					}
				});

				xhr.addEventListener('error', () => reject(new Error('Upload failed')));

				xhr.open('POST', 'http://localhost:8000/upload-doc');
				xhr.send(formData);
			});

			const response = await uploadFile;

			// Handle successful upload
			const completeDoc = {
				file_id: response.file_id,
				filename: file.name,
				upload_timestamp: new Date().toISOString(),
				...response
			};
			documentStore.value = [...documentStore.value, completeDoc];

			// Reset file input
			if (fileInput) fileInput.value = '';
		} catch (error) {
			console.error('Upload error:', error);
			uploadError = error instanceof Error ? error.message : 'Upload failed';
		} finally {
			isUploading = false;
		}
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
</script>

<div class="document-manager">
	<div class="documents-section">
		<div>
			<h2 class="title">Available Documents</h2>
		</div>

		<div class="upload-section">
			<input
				type="file"
				accept=".pdf"
				onchange={(e) => handleFileUpload(e)}
				bind:this={fileInput}
				disabled={isUploading}
			/>
			{#if isUploading}
				<div class="upload-progress">
					<div class="progress-bar">
						<div class="progress-fill" style="width: {uploadProgress}%"></div>
					</div>
					<div class="progress-text">{uploadProgress}%</div>
				</div>
			{/if}
			{#if uploadError}
				<div class="error-message" role="alert">
					{uploadError}
				</div>
			{/if}
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
					<div class="documents-cell">{doc.filename}</div>
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
	.upload-progress {
		margin-top: 0.5rem;
	}
	.progress-bar {
		width: 100%;
		height: 4px;
		background: var(--surface-2);
		border-radius: 2px;
		overflow: hidden;
	}
	.progress-fill {
		height: 100%;
		background: var(--accent-1);
		transition: width 0.2s ease;
	}
	.progress-text {
		font-size: 0.875rem;
		color: var(--text-2);
		margin-top: 0.25rem;
	}
	.progress-fill {
		height: 100%;
		background: var(--accent-1);
		transition: width 0.3s ease-out;
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
		margin-bottom: 1rem;
	}
	.document-manager {
		margin-bottom: 1rem;
	}

	.upload-section {
		justify-self: end;
	}
	.upload-status {
		color: var(--text-2);
		margin-top: 0.5rem;
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
