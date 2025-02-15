import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, depends }) => {
	console.log('Load function running');
	depends('/list-docs');
	depends('list-docs');
	depends('http://localhost:8000/list-docs');
	depends('*/list-docs');

	try {
		const [docsResponse] = await Promise.all([fetch('http://localhost:8000/list-docs')]);

		if (!docsResponse.ok) {
			throw new Error('One or more API calls failed');
		}

		const docsData = await docsResponse.json();

		return {
			listDocuments: docsData,
			error: null
		};
	} catch (error) {
		console.error('Error loading data:', error);
		return {
			listDocuments: null,
			error: 'Failed to load data. Please try again later.'
		};
	}
};
