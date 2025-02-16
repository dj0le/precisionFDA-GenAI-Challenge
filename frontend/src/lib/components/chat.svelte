<script lang="ts">
	import { storedModel } from '$lib/stores';
	import Markdown from './markdown.svelte';
	import { v4 as uuidv4 } from 'uuid';

	let question = '';
	let answer = '';
	let sources = {};
	let response_metadata = {};
	let usage_metadata = {};
	let isLoading = false;
	let sessionId = uuidv4();

	function formatDuration(nanoseconds: number): string {
		const seconds = nanoseconds / 1_000_000_000;
		const minutes = Math.floor(seconds / 60);
		const remainingSeconds = seconds % 60;
		return minutes > 0
			? `${minutes}m ${remainingSeconds.toFixed(2)}s`
			: `${remainingSeconds.toFixed(2)}s`;
	}

	async function handleSubmit() {
		isLoading = true;
		try {
			console.log('Submitting with:', {
				question,
				model: storedModel.value,
				session_id: sessionId
			});

			const response = await fetch('http://localhost:8000/chat', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					question,
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

			question = '';
		} catch (error) {
			console.error('Error:', error);
			answer = 'Error: Failed to get response';
		} finally {
			isLoading = false;
		}
	}
</script>

<div class="chat-container">
	{#if isLoading}
		<div>thinking...</div>
	{:else}
		<div class="question">
			<h3 class="question-label title">Question:</h3>
			<div class="question-text">{question}</div>
		</div>
		<div class="separator"></div>
		<div class="answer">
			<h3 class="answer-label title">Feddi:</h3>
			<div class="answer-text"><Markdown content={answer} /></div>
		</div>
		<div class="separator"></div>
		<div class="sources">
			<h3 class="sources-label title">Sources:</h3>
			<div class="sources-container">
				<div class="sources-list">
					<ul>
						{#each sources as source}
							<li>{source}</li>
						{/each}
					</ul>
				</div>
				<div class="sources-details">
					<div>
						Processing Time: {formatDuration(response_metadata.total_duration)}
					</div>
					<div>
						Tokens Used: {usage_metadata.total_tokens}
					</div>
				</div>
				<button class="sources-button button">clear chat</button>
			</div>
		</div>
	{/if}
</div>
<div class="question-container">
	<div>
		<form on:submit|preventDefault={handleSubmit}>
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
		display: grid;
		grid-template-columns: 1fr;
		grid-template-rows: auto auto auto;
		max-width: 1600px;
		width: 100%;
		align-items: start;
	}
	.question,
	.answer,
	.sources {
		display: grid;
		grid-template-columns: 1fr auto;
		grid-gap: 8px;
		padding-block: 16px;
	}
	.answer-label,
	.sources-label,
	.question-label {
		align-self: start;
	}
	.answer-text {
		justify-self: start;
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
	.question-container {
		width: 100%;
		padding: 16px;
		margin-top: 32px;
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
