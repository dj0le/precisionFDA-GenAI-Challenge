<script lang="ts">
	import MdiGithub from '~icons/mdi/github';
</script>

<footer>
	<div class="footer-content">
		<a
			href="https://github.com/dj0le/precisionFDA-GenAI-Challenge"
			class="github-link"
			target="_blank"
			rel="noopener noreferrer"
		>
			<MdiGithub style="font-size: 2em; color: var(--accent-1)" />
			<span>Visit project page</span>
		</a>
		<a
			href="https://www.space-shift.com/"
			class="page-link"
			target="_blank"
			rel="noopener noreferrer">2025 // SPACEshift</a
		>
	</div>
</footer>

<style>
	footer {
		padding-block: 12px;
	}
	.footer-content {
		display: grid;
		grid-template-columns: auto auto;
		gap: 40px;
		align-items: center;
		justify-content: start;
	}
	.github-link {
		display: flex;
		align-items: center;
		gap: 8px;

		color: inherit;
	}
	.page-link {
		color: inherit;
	}
</style>
