import { localStore } from './localStore.svelte';

export const storedModel = localStore('storedModel', 'llama3.2');
export const availableModels = localStore<[]>('availableModels', []);
