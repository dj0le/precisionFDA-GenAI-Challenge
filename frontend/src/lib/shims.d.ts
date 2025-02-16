declare module '~icons/*' {
	import { SvelteComponentTyped } from 'svelte';
	import { HTMLAttributes } from 'svelte/elements';

	interface IconProps extends HTMLAttributes<SVGSVGElement> {
		width?: string | number;
		height?: string | number;
		color?: string;
	}

	const component: new () => SvelteComponentTyped<IconProps>;
	export default component;
}
