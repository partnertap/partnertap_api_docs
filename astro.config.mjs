// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://dev.partnertap.com',
	base: '/',
	integrations: [
		starlight({
			title: 'PartnerTap API Docs',
			logo: {
				light: './src/assets/PartnerTap_Logo_Light.png',
				dark: './src/assets/PartnerTap_Logo_Dark.png',
				replacesTitle: false
			},
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
