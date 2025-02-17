<script lang="ts">
	import { storedModel } from '$lib/stores';
	import Markdown from '$lib/components/markdown.svelte';
	import { v4 as uuidv4 } from 'uuid';

	let hasAskedQuestion = false;
	let question = '';
	let displayedQuestion = '';
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
		hasAskedQuestion = true;
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

			displayedQuestion = question;
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
	{#if !hasAskedQuestion}
		<div class="placeholder-message">
			<h3 class="title">Hello, I'm Feddi</h3>
			<p>
				I'm your guide to FDA related questions. If this is your first time using the app, here's a
				few tips:
			</p>
			<p>
				On the top right, select the chat model you w to use. I'm a fan ofllama 3.2, but any chat
				model will work, and you can change it anytime.
			</p>
			<p>
				There are 3 sections to this app, this one is for chatting. If you would like to add
				documents to my database, choose the documents section. You can also see all the documents
				currentlyin the database, or delete any that are no longer needed.
			</p>
			<p>
				The info section will give more details about the project and participants. You can also
				verify that the app is up and running (look for th healthy green heart). And, you can see a
				list of all the local models on your system that the app can see to ensure the ones you want
				are available.
			</p>
			<p>
				When ready, simply come back to this chat page, and at the bottom input whatever questions
				you have
			</p>
			<p>Example questions:</p>
			<ul>
				<li>
					How does the FDA define "insanitary conditions" in the preparation, packing, and holding
					of tattoo inks?
				</li>
				<li>What is the numeric code for eye liner?</li>
				<li>What are common mistakes with non compliance when starting a cosmetic business??</li>
			</ul>
			<p>
				I will always attempt to use the local documents to answer your questions, to ensure as much
				accuracy as possible
			</p>
			<p>I look forward to interacting with you!</p>
			<h3 class="title">-Feddi</h3>
		</div>
	{:else if isLoading}
		<div>thinking...</div>
	{:else}
		<div class="question">
			<h3 class="question-label title">Question:</h3>
			<div class="question-text">{displayedQuestion}</div>
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
				<div class="clear-container">
					<button class="sources-button button">clear chat</button>
				</div>
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
		max-width: 1200px;
		width: 100%;
		align-items: start;
		margin-inline: auto;
	}
	.question,
	.answer,
	.sources {
		display: grid;
		grid-template-columns: 15% 1fr;
		grid-gap: 8px;
		padding-block: 16px;
		justify-items: center;
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
