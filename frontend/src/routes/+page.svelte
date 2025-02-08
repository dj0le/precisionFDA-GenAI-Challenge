<script lang="ts">
	let { data } = $props();
	const { health, documents } = data;
</script>

<h1>Welcome to Cosmeticky</h1>
<p>Answer your FDA related questions</p>

{#if health}
	<div>
		<h2>System Status</h2>
		<p>Status: {health.status}</p>
		<p>API Version: {health.api_version}</p>
		<p>Models Loaded:</p>
		<ul>
			{#each health.models_loaded as model}
				<li>{model}</li>
			{/each}
		</ul>
	</div>
{/if}

{#if documents && documents.length > 0}
	<div class="documents-section">
		<h2>Available Documents</h2>
		<div class="grid-table">
			<div class="grid-header">
				<div class="cell">File ID</div>
				<div class="cell">Filename</div>
				<div class="cell">Upload Date</div>
			</div>
			{#each documents as doc}
				<div class="row">
					<div class="cell">{doc.file_id}</div>
					<div class="cell">{doc.filename}</div>
					<div class="cell">{new Date(doc.upload_timestamp).toLocaleString()}</div>
				</div>
			{/each}
		</div>
	</div>
{:else}
	<p>No documents available</p>
{/if}

<style>
	.documents-section {
		margin-block: 2rem;
	}

	.grid-table {
		display: grid;
		grid-template-columns: 1fr;
		gap: 2px;
		background-color: hsl(220, 13%, 90%);
		border-radius: 6px;
		overflow: hidden;
	}

	.grid-header {
		display: grid;
		grid-template-columns: auto 1fr auto;
		gap: 2px;
		background-color: hsl(220, 13%, 90%);
		font-weight: 600;
	}

	.row {
		display: grid;
		grid-template-columns: auto 1fr auto;
		gap: 2px;
		background-color: white;
		transition: background-color 200ms ease;
	}

	.row:hover {
		background-color: hsl(220, 13%, 98%);
	}

	.cell {
		padding: clamp(0.5rem, 2vw, 1rem);
		color: hsl(220, 13%, 20%);
	}
</style>
