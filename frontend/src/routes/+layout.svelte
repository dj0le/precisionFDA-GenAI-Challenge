<script lang="ts">
	import Header from './header.svelte';
	import Footer from './footer.svelte';

	let { children } = $props();

	import 'open-props/style';
	import 'open-props/normalize';
	import '../app.css';
</script>

<div class="layout">
	<Header />
	<main>
		{@render children()}
	</main>

	<Footer />
</div>

<style>
	.layout {
		height: 100%;
		min-height: 100vh;
		display: grid;
		grid-template-rows: auto 1fr auto;
		align-items: center;
		justify-content: center;
		align-content: space-between;
		margin-inline: auto;
		padding-inline: 2rem;
	}
</style>
