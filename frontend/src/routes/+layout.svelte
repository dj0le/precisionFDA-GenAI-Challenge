<script lang="ts">
	import Header from './header.svelte';
	import Footer from './footer.svelte';

	let { children } = $props();

	import 'open-props/style';
	import 'open-props/normalize';
	import '../app.css';
</script>

<svelte:head>
	<title>Feddi /guide</title>
</svelte:head>

<div class="layout">
	<Header />
	<main>
		{@render children()}
	</main>
</div>

<style>
	.layout {
		position: relative;
		height: 100%;
		min-height: 100vh;
		display: grid;
		grid-template-rows: auto 1fr;
		align-items: center;
		justify-content: center;
		align-content: space-between;
		margin-inline: auto;
		padding-inline: 2rem;
		border: 2px solid var(--border-1);
	}
</style>
