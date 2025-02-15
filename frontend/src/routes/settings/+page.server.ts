import type { PageServerLoad } from './$types';
export const load: PageServerLoad = async ({ fetch }) => {
	try {
		const [healthResponse] = await Promise.all([fetch('http://localhost:8000/health')]);

		if (!healthResponse.ok) {
			throw new Error('One or more API calls failed');
		}

		const healthData = await healthResponse.json();

		return {
			health: healthData,
			error: null
		};
	} catch (error) {
		console.error('Error loading data:', error);
		return {
			health: null,
			error: 'Failed to load data. Please try again later.'
		};
	}
};
