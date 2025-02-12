<script lang="ts">
	import type { Document } from '$lib/types';

	let { listDocuments, refreshDocuments } = $props<{
		listDocuments: Document[];
		refreshDocuments: () => Promise<void>;
	}>();

	let fileInput: HTMLInputElement;
	let isUploading = $state(false);
	let uploadError = $state('');

	let displayDocuments = $derived(
		listDocuments.map((doc, index) => ({
			...doc,
			displayIndex: index + 1
		}))
	);

	async function handleFileUpload(event: Event) {
		const input = event.target as HTMLInputElement;
		if (!input.files?.length) return;

		const file = input.files[0];
		isUploading = true;
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
				console.log('Error data received:', errorData);

				if (errorData.detail?.includes('File already exists with ID:')) {
					uploadError = 'This document has already been uploaded.';
				} else {
					uploadError = errorData.detail || 'Upload failed';
				}
				console.log('Upload error set to:', uploadError);
				return;
			}

			if (response.ok) {
				console.log('Before refreshDocuments call');
				await refreshDocuments();
				console.log('After refreshDocuments call');
			}

			// Reset file input
			if (fileInput) fileInput.value = '';
		} catch (error) {
			console.error('Upload error:', error);
			uploadError = error instanceof Error ? error.message : 'Upload failed';
			console.log('Catch block upload error set to:', uploadError);
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
				const result = await response.json();
				console.log('Delete successful:', result);
				await refreshDocuments();
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
				<div class="upload-status">Uploading...</div>
			{/if}
			{#if uploadError}
				<div class="error-message" role="alert">
					{uploadError}
				</div>
			{/if}
		</div>
	</div>

	{#if listDocuments && listDocuments.length > 0}
		<div class="documents-grid">
			<div class="documents-header">
				<div class="documents-cell">Number</div>
				<div class="documents-cell">Filename</div>
				<div class="documents-cell">Uploaded</div>
				<div class="documents-cell"></div>
			</div>
			{#each displayDocuments as doc}
				<div class="documents-row">
					<div class="documents-cell">{doc.displayIndex}</div>
					<div class="documents-cell">{doc.filename}</div>
					<div class="documents-cell">{new Date(doc.upload_timestamp).toLocaleString()}</div>
					<div class="documents-cell">
						<button class="delete-button" onclick={() => handleDelete(doc.file_id)}>
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
	.delete-button {
		background-color: var(--error);
		color: white;
		border: none;
		padding: 0.5rem 1rem;
		border-radius: 4px;
		cursor: pointer;
	}
	.delete-button:hover {
		background-color: #c42126;
	}
</style>
