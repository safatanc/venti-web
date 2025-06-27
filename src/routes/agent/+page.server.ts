import type { PageServerLoad } from './$types';
import { JKT48_MEMBERS, type Member } from '$lib/data/jkt48';

export const load: PageServerLoad = async () => {
	const members: Member[] = JKT48_MEMBERS;

	return {
		members
	};
};
