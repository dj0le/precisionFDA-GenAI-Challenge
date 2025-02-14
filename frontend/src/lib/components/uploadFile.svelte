<script lang="ts">
	let { onUpload } = $props<{ onUpload: (files: File[]) => void }>();
	let files: File[] = $state([]);
	let fileNames: string[] = $derived(files.map((file) => file.name));
	let dragging = $state(false);

	function handleFileSelect(event: Event) {
		const target = event.target as HTMLInputElement;
		if (target.files) {
			files = Array.from(target.files);
			onUpload(files);
		}
	}

	function handleDrop(event: DragEvent) {
		event.preventDefault();
		dragging = false;
		const dataTransfer = event.dataTransfer;
		if (dataTransfer && dataTransfer.files) {
			files = Array.from(dataTransfer.files);
			onUpload(files);
		}
	}

	function handleDragOver(event: Event) {
		event.preventDefault();
		dragging = true;
	}

	function handleDragLeave(event: Event) {
		event.preventDefault();
		dragging = false;
	}

	function handleDragEnter(event: Event) {
		event.preventDefault();
		dragging = true;
	}

	function handleClick() {
		document.getElementById('file-input')?.click();
	}

	function handleKeyDown(event: KeyboardEvent) {
		if (event.key === 'Enter' || event.key === ' ') {
			document.getElementById('file-input')?.click();
		}
	}
</script>

<div
	class="upload-area"
	class:dragging
	ondrop={handleDrop}
	ondragover={handleDragOver}
	ondragleave={handleDragLeave}
	ondragenter={handleDragEnter}
	onclick={handleClick}
	onkeydown={handleKeyDown}
	tabindex="0"
	role="button"
>
	{#if files.length > 0}
		<div class="file-list">
			{#each fileNames as fileName}
				<span class="file-name">{fileName}</span>
			{/each}
		</div>
	{:else if dragging}
		<p>Drop files here...</p>
	{:else}
		<p>Drag & drop files here or</p>
		<div class="upload-button">UPLOAD FILE</div>
	{/if}

	<input type="file" id="file-input" multiple onchange={handleFileSelect} style="display:none;" />
</div>

<style>
	.upload-area {
		background: var(--surface-2);
		border: 1px solid var(--border-1);
		border-radius: 6px;
		padding: 24px;
		text-align: center;
		cursor: pointer;
		width: 300px;
		margin: 20px auto;
		transition: background-color 0.1s ease-in-out;
	}
	.upload-area.dragging {
		border-color: var(--border-1);
		background-color: var(--surface-2);
	}
	/* .file-list {
		margin-top: 10px;
	} */

	.file-name {
		display: inline-block;
		margin: 8px;
		padding: 8px 16px;
		border: 1px solid #ddd;
		border-radius: 6px;
		background-color: var(--surface-2);
	}
	.upload-area:hover {
		background-color: var(--surface-1);
	}
	.upload-button {
		margin-block: 16px;
		padding: 8px 16px;
		border-radius: 6px;
		background-color: var(--surface-6);
	}
	.upload-button:hover {
		outline: 2px solid var(--border-1);
		outline-offset: 6px;
		border-radius: 6px;
		background-color: var(--surface-6);
		transition: 0.2s all ease;
	}
</style>
