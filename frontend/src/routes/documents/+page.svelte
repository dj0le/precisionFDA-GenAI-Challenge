<script lang="ts">
	import { documentStore } from '$lib/stores';
	import DocumentManager from '$lib/components/documentManager.svelte';

	let { data } = $props();
	const { listDocuments } = data;

	$effect(() => {
		if (listDocuments) {
			documentStore.value = listDocuments;
		}
	});
</script>

<div class="documents-section">
	<DocumentManager listDocuments={documentStore.value} />
</div>
