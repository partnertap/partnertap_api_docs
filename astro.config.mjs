// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://partnertap.github.io',
	base: '/partnertap_api_docs',
	integrations: [
		starlight({
			title: 'PartnerTap API Docs',
			social: [
				{
					icon: 'github',
					label: 'GitHub',
					href: 'https://github.com/partnertap/partnertap_api_docs',
				},
			],
			sidebar: [
				{
					label: 'API Guides',
					items: [{ autogenerate: { directory: 'guides' } }],
				},
				{
					label: 'Code Examples',
					items: [{ autogenerate: { directory: 'examples' } }],
				},
			],
		}),
	],
});
