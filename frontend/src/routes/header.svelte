<div class="primary">
	<div><a href="/"><img src="./header1.svg" alt="feddi /guide" class="logo" /></a></div>
	<nav>
		<ul>
			<li>
				<a href="/">
					<img src="./chat.svg" alt="Chat" />
					<span>chat</span>
				</a>
			</li>
			<li>
				<a href="/documents">
					<img src="./docs.svg" alt="Documents" />
					<span>documents</span>
				</a>
			</li>
			<li>
				<a href="/settings">
					<img src="./settings.svg" alt="Info" />
					<i class="fas fa-cog"></i>
					<span>info</span>
				</a>
			</li>
		</ul>
	</nav>
</div>

<style>
	.primary {
		display: grid;
		grid-template-columns: 1fr;
		justify-content: center;
		place-items: center;
		gap: 8px;
		margin-block: 16px;
	}
	nav ul {
		list-style: none;
		padding: 0;
		display: flex;
		gap: 1rem;
	}
	nav a {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.75rem 1rem;
		text-decoration: none;
		color: var(--accent-2);
		border-radius: 8px;
		transition: background-color 0.25s ease-in-out;
	}
	nav a:hover {
		background-color: var(--surface-2);
	}
</style>
