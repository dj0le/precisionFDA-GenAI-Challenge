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
		<p>Drag & drop files here or click to select</p>
	{/if}

	<input type="file" id="file-input" multiple onchange={handleFileSelect} style="display:none;" />
</div>

<style>
	.upload-area {
		border: 2px dashed #ccc;
		padding: 20px;
		text-align: center;
		cursor: pointer;
		width: 300px;
		margin: 20px auto;
		transition: border-color 0.2s ease;
	}

	.upload-area.dragging {
		border-color: #007bff;
		background-color: #f0f8ff;
	}

	.file-list {
		margin-top: 10px;
	}

	.file-name {
		display: inline-block;
		margin: 5px;
		padding: 5px 10px;
		border: 1px solid #ddd;
		border-radius: 4px;
		background-color: #f9f9f9;
	}

	.upload-area:hover {
		border-color: #007bff;
	}

	p {
		margin: 0;
	}
</style>
