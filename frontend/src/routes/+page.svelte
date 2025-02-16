<script lang="ts">
	import Chat from '$lib/components/chat.svelte';
</script>

<div class="container">
	<div class="chat-section">
		<Chat />
	</div>
</div>

<style>
	.chat-section {
		margin-block: 2rem;
		border-radius: 6px;
		padding: var(--padding);
	}
</style>
