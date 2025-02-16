<script lang="ts">
	import Header from './header.svelte';

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
	<main class="main">
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
		align-content: space-between;
		padding-inline: 2rem;
	}
	main {
		margin-top: 8rem;
		padding-inline: 2rem;
		align-self: start;
		width: 100%;
	}
</style>
