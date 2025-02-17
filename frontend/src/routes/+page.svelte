<script lang="ts">
	import { storedModel } from '$lib/stores';
	import Markdown from '$lib/components/markdown.svelte';
	import { v4 as uuidv4 } from 'uuid';
	import Placeholder from '$lib/components/welcomeMessage.svelte';

	// Runes-based state management
	let hasAskedQuestion = $state(false);
	let question = $state('');
	let displayedQuestion = $state('');
	let answer = $state('');
	let sources = $state({});
	let response_metadata = $state({});
	let usage_metadata = $state({});
	let isLoading = $state(false);
	let sessionId = $state(uuidv4());
	let currentContent = $state('');
	let chatContainerHeight = $state('58vh');

	function formatDuration(nanoseconds: number): string {
		const seconds = nanoseconds / 1_000_000_000;
		const minutes = Math.floor(seconds / 60);
		const remainingSeconds = seconds % 60;
		return minutes > 0
			? `${minutes}m ${remainingSeconds.toFixed(2)}s`
			: `${remainingSeconds.toFixed(2)}s`;
	}

	async function handleSubmit(event: Event) {
		event.preventDefault();
		isLoading = true;
		hasAskedQuestion = true;
		currentContent = 'thinking...';

		try {
			const response = await fetch('http://localhost:8000/chat', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					question: question,
					model: storedModel.value,
					session_id: sessionId
				})
			});

			if (!response.ok) {
				const errorData = await response.json();
				console.error('API Error:', errorData);
				throw new Error(JSON.stringify(errorData.detail));
			}

			const result = await response.json();

			answer = result.answer;
			sources = result.sources;
			response_metadata = result.response_metadata;
			usage_metadata = result.usage_metadata;

			displayedQuestion = question;
			question = '';
			currentContent = 'answer';
		} catch (error) {
			console.error('Error:', error);
			answer = 'Error: Failed to get response';
			currentContent = 'error';
		} finally {
			isLoading = false;
		}
	}

	function clearChat() {
		hasAskedQuestion = false;
		question = '';
		displayedQuestion = '';
		answer = '';
		sources = {};
		response_metadata = {};
		usage_metadata = {};
		isLoading = false;
		sessionId = uuidv4();
		currentContent = '';
		chatContainerHeight = '58vh';
	}
</script>

<div class="chat-container" style="min-height: {chatContainerHeight}">
	{#if !hasAskedQuestion && currentContent === ''}
		<div class="fade-in">
			<Placeholder />
		</div>
	{:else if isLoading && currentContent === 'thinking...'}
		<div class="fade-in">thinking...</div>
	{:else if currentContent === 'answer'}
		<div class="fade-in question">
			<h3 class="question-label title">Question:</h3>
			<div class="question-text">{displayedQuestion}</div>
		</div>
		<div class="fade-in separator"></div>
		<div class="fade-in answer">
			<h3 class="answer-label title">Feddi:</h3>
			<div class="answer-text">
				<Markdown content={answer} />
			</div>
		</div>
		<div class="fade-in separator"></div>
		<div class="fade-in sources">
			<h3 class="sources-label title">Sources:</h3>
			<div class="sources-container">
				<div class="sources-list">
					<ul>
						{#each Object.entries(sources) as [key, source]}
							<li {key}>{source}</li>
						{/each}
					</ul>
				</div>
				<div class="sources-details">
					<div>Processing Time: {formatDuration(response_metadata.total_duration)}</div>
					<div>Tokens Used: {usage_metadata.total_tokens}</div>
				</div>
				<div class="clear-container">
					<button class="sources-button button" onclick={clearChat}>clear chat</button>
				</div>
			</div>
		</div>
	{:else if currentContent === 'error'}
		<div class="fade-in">Error: Failed to get Response</div>
	{/if}
</div>

<div class="question-container">
	<div>
		<form onsubmit={handleSubmit}>
			<label class="field auto-fit">
				<span class="label">User:</span>
				<input
					type="text"
					bind:value={question}
					placeholder="Ask a question..."
					disabled={isLoading}
				/>
			</label>
		</form>
	</div>
</div>

<style>
	.chat-container {
		border: 1px solid var(--border-1);
		background-color: var(--surface-2);
		border-radius: 6px;
		padding: var(--padding);
		display: flex;
		flex-direction: column;
		max-width: 1200px;
		width: 100%;
		overflow-y: auto;
		align-items: stretch; /* Changed from start to stretch*/
		margin-inline: auto;
		position: relative;
		overflow: visible;
		min-height: 58vh;
	}

	.fade-in {
		animation: fadeIn 0.3s ease-in-out;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
		}

		to {
			opacity: 1;
		}
	}

	.question,
	.sources {
		display: grid;
		grid-template-columns: 15% 1fr;
		grid-gap: 8px;
		padding-block: 16px;
		justify-items: start;
		flex: 0 0 auto;
		align-items: start;
	}

	.answer {
		display: grid;
		grid-template-columns: 15% 1fr;
		grid-gap: 8px;
		padding-block: 16px;
		justify-items: start;
		flex: 1;
		align-items: start;
	}

	.answer-label,
	.sources-label,
	.question-label {
		align-self: start;
	}

	.question-text,
	.answer-text,
	.sources-container {
		margin-left: 16px;
		justify-self: start;
	}

	.answer-text {
		height: 100%;
	}

	.separator {
		border: 1px solid var(--border-1);
	}

	.sources-container {
		display: grid;
		grid-template-columns: 1fr 1fr 1fr;
		gap: 8px;
		padding-top: 32px;
	}

	.sources-button {
		background-color: var(--surface-1);
	}

	.sources-details {
		place-self: center;
	}

	.clear-container {
		place-self: end;
	}

	.question-container {
		width: 100%;
		max-width: 1200px;
		padding-block: 16px;
		margin-top: 32px;
		margin-inline: auto;
	}

	.question-container form label {
		color: var(--accent-1);
		margin-bottom: 8px;
		padding-left: 18px;
	}

	.question-container form input[type='text'] {
		padding: 16px;
		background-color: var(--surface-2);
		border: 1px solid var(--border-1);
		border-radius: 6px;
		width: 100%;
	}
</style>
