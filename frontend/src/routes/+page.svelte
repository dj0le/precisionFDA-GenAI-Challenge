<script lang="ts">
	import Chat from '$lib/components/chat.svelte';
</script>

<div class="container">
	<div class="chat-section">
		<Chat />
	</div>
</div>

<style>
	.container {
		border: 1px solid var(--border-1);
		border-radius: 6px;
		padding: var(--padding);
	}
	.chat-section {
		margin-block: 2rem;
		border-radius: 6px;
		padding: var(--padding);
	}
</style>
