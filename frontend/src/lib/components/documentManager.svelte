<script lang="ts">
	import { documentStore } from '$lib/stores';
	import type { Document } from '$lib/types';
	import type { ToastType } from '$lib/types';
	import UploadFile from './uploadFile.svelte';
	import Toast from './toast.svelte';
	import { onMount } from 'svelte';
	import DocumentList from './documentList.svelte';

	export interface DisplayDocument extends Document {
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

	let sortField = $state('upload_timestamp');
	let sortDirection = $state<'asc' | 'desc'>('desc');
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
		const uploadedFileNames = files.map((file) => file.name).join(', ');
		let allUploadsSuccessful = true;

		for (const file of files) {
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
						toastMessage = `${file.name}: ${errorMessage}`;
						toastType = 'info';
						allUploadsSuccessful = false;
					} else {
						toastMessage = `Error uploading ${file.name}: ${errorMessage}`;
						toastType = 'error';
						allUploadsSuccessful = false;
					}
					await new Promise((resolve) => setTimeout(resolve, 3000));
					toastMessage = '';
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
				allUploadsSuccessful = false;
				await new Promise((resolve) => setTimeout(resolve, 3000));
				toastMessage = '';
			}
		}
		if (allUploadsSuccessful) {
			toastMessage = `Uploaded: ${uploadedFileNames}`;
			toastType = 'success';
			await new Promise((resolve) => setTimeout(resolve, 3000));
			toastMessage = '';
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
				toastMessage = errorData.detail || 'Delete failed';
				toastType = 'error';
				await new Promise((resolve) => setTimeout(resolve, 3000));
				toastMessage = '';
				return;
			}

			if (response.ok) {
				documentStore.value = documentStore.value.filter((doc) => doc.file_id !== fileId);
				toastMessage = 'Document deleted successfully.';
				toastType = 'success';
				await new Promise((resolve) => setTimeout(resolve, 3000));
				toastMessage = '';
			}
		} catch (error) {
			console.error('Delete error:', error);
			toastMessage = error instanceof Error ? error.message : 'The document could not be deleted.';
			toastType = 'warning';
			await new Promise((resolve) => setTimeout(resolve, 3000));
			toastMessage = '';
		}
	}

	onMount(() => {
		console.log('listDocuments: ', $inspect(listDocuments));
	});
</script>

{#if toastMessage}
	<Toast message={toastMessage} type={toastType} />
{/if}

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

	{#if documentStore.value.length > 0}
		<DocumentList
			{displayDocuments}
			{sortField}
			{sortDirection}
			onSort={handleSort}
			onDelete={handleDelete}
		/>
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
</style>
