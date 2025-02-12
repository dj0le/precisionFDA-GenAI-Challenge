import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, depends }) => {
	console.log('Load function running');
	depends('/list-docs');
	depends('list-docs');
	depends('http://localhost:8000/list-docs');
	depends('*/list-docs');

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
		console.log('Fresh data loaded:', docsData);

		return {
			health: healthData,
			listDocuments: docsData,
			error: null
		};
	} catch (error) {
		console.error('Error loading data:', error);
		return {
			health: null,
			listDocuments: null,
			error: 'Failed to load data. Please try again later.'
		};
	}
};
