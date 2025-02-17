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
		<div class="placeholder">
			<div>
				<h2 class="title">Hello, I'm Feddi</h2>

				<p class="gap">
					I'm your guide to FDA related questions. If this is your first time using the app, here's
					a few tips:
				</p>
				<div class="model-info">
					<p class="sub-title gap">1. Select a model</p>
					<p>
						On the top right, select the chat model you want to use. I'm a fan of Llama 3.2, but any
						chat model will work. Change it anytime.
					</p>
					<p class="sub-title gap">2. Upload your documents</p>
					<p>
						If you haven't already, you'll need to add your pdf documents to the database in the
						document section.
					</p>
					<p class="sub-title gap">3. Ask your questions</p>
					<p>
						Once you've selected a model, you can start asking questions. I'll do my best to provide
						you with accurate and helpful information.
					</p>
				</div>
				<div>
					<p class="sub-title gap">Examples</p>
					<ul>
						<li>
							How does the FDA define "insanitary conditions" in the preparation, packing, and
							holding of tattoo inks?
						</li>
						<li>What is the numeric code for eye liner?</li>
						<li>
							What are common mistakes with non compliance when starting a cosmetic business??
						</li>
					</ul>
				</div>
			</div>
			<div class="column-right">
				<h3 class="title">The app has 3 sections:</h3>
				<div class="chat-info">
					<p class="sub-title gap">1. Chat</p>
					<p>
						This the main page and where you can ask me your questions. Use the input at the bottom.
					</p>
				</div>
				<div class="document-info">
					<p class="sub-title gap">2. Documents</p>
					<p>
						This is where you can add or delete documents. All current documents will be displayed
						in the list. Use the search feature to find specific documents. You can also sort by
						name or upload date.
					</p>
				</div>
				<div class="info-info">
					<p class="sub-title gap">3. Info</p>
					<p>
						Details the project and participants. You can also verify that the app is up and running
						(look for th healthy green heart). And, you can see a list of all the local models on
						your system.
					</p>
				</div>
				<p class="gap">I look forward to interacting with you!</p>
				<h3 class="title gap sig">-Feddi</h3>
			</div>
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
	.gap {
		margin-top: 16px;
	}
	.sig {
		text-align: right;
		padding-right: 32px;
	}
	.sub-title {
		font-size: var(--font-size-sub-title);
	}
	.placeholder {
		padding: 16px;
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 32px;
	}
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
