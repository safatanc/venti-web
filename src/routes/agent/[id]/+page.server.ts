import type { PageServerLoad } from './$types';
import { JKT48_MEMBERS, type Member } from '$lib/data/jkt48';

export const load: PageServerLoad = async ({
	params
}: {
	params: { id: string };
	fetch: typeof window.fetch;
}) => {
	const members: Member[] = JKT48_MEMBERS;

	const member = members.find((member: Member) => member.id === params.id);

	return {
		member
	};
};
