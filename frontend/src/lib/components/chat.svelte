<script lang="ts">
	import { storedModel } from '$lib/stores';
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
			// console.log('Full response:', result);

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
	<div class="llm-section">
		{#if isLoading}
			<div>Loading...</div>
		{:else}
			<div class="chat-answer">{answer}</div>
			<div class="chat-additional">
				Sources:
				<ul>
					{#each sources as source}
						<li>{source}</li>
					{/each}
				</ul>
			</div>
			<div class="chat-additional">
				Processing Time: {response_metadata?.total_duration
					? formatDuration(response_metadata.total_duration)
					: 'N/A'}
			</div>
			<div class="chat-additional">
				Tokens Used: {usage_metadata.total_tokens}
			</div>
		{/if}
	</div>
	<div class="user-input">
		<form on:submit|preventDefault={handleSubmit}>
			<input
				type="text"
				bind:value={question}
				placeholder="Ask a question..."
				disabled={isLoading}
			/>
			<button type="submit" disabled={isLoading}>
				{isLoading ? 'Sending...' : 'Send'}
			</button>
		</form>
	</div>
</div>

<style>
	.chat-additional {
		padding-block: 16px;
	}
</style>
