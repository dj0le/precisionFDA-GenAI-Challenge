import { browser } from '$app/environment';

export class LocalStore<T> {
	value = $state<T>() as T;
	key = '';

	constructor(key: string, initialValue: T) {
		this.key = key;

		if (browser) {
			const item = localStorage.getItem(key);
			this.value = item ? this.deserialize(item) : initialValue;
		} else {
			this.value = initialValue;
		}
	}

	serialize(value: T): string {
		return JSON.stringify(value);
	}

	deserialize(item: string): T {
		return JSON.parse(item);
	}
}

export function localStore<T>(key: string, value: T) {
	const store = new LocalStore(key, value);

	if (browser) {
		$effect.root(() => {
			$effect(() => {
				localStorage.setItem(store.key, store.serialize(store.value));
			});
		});
	}

	return store;
}
