import { localStore } from './localStore.svelte';
import type { Document } from '$lib/types';

export const storedModel = localStore('storedModel', 'llama3.2');
export const availableModels = localStore<[]>('availableModels', []);
export const documentStore = localStore<Document[]>('documents', []);
