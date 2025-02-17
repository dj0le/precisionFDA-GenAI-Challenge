<script lang="ts">
	import Header from './header.svelte';
	import 'open-props/style';
	import 'open-props/normalize';
	import '../app.css';

	let { children } = $props();

	import { availableModels } from '$lib/stores';

	export const load = async () => {
		try {
			const healthResponse = await fetch('http://localhost:8000/health');

			if (!healthResponse.ok) {
				throw new Error('Health API call failed');
			}

			const healthData = await healthResponse.json();

			if (healthData?.models_loaded) {
				availableModels.value = healthData.models_loaded;
			}

			return {};
		} catch (error) {
			console.error('Error loading health data:', error);
			availableModels.value = [];
			return {};
		}
	};
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
		margin-inline: auto;
		padding-inline: 2rem;
		max-width: 1600px;
	}
	main {
		margin-top: 8rem;
		padding-inline: 2rem;
		align-self: start;
		width: 100%;
	}
</style>
