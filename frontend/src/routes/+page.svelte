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
	<div>
		<h2>Available Documents</h2>
		<table>
			<thead>
				<tr>
					<th>File ID</th>
					<th>Filename</th>
					<th>Upload Date</th>
				</tr>
			</thead>
			<tbody>
				{#each documents as doc}
					<tr>
						<td>{doc.file_id}</td>
						<td>{doc.filename}</td>
						<td>{new Date(doc.upload_timestamp).toLocaleString()}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{:else}
	<p>No documents available</p>
{/if}
