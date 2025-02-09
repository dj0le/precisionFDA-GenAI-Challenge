export async function load({ fetch }) {
	try {
		const [healthResponse, docsResponse] = await Promise.all([
			fetch('http://localhost:8000/health'),
			fetch('http://localhost:8000/list-docs')
		]);

		if (!healthResponse.ok || !docsResponse.ok) {
			throw new Error('One or more API calls failed');
		}

		const healthData = await healthResponse.json();
		const docsData = await docsResponse.json();

		return {
			health: healthData,
			documents: docsData,
			error: null
		};
	} catch (error) {
		console.error('Error loading data:', error);
		return {
			health: null,
			documents: null,
			error: 'Failed to load data. Please try again later.'
		};
	}
}
