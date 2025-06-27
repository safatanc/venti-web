export type Member = {
	id: string;
	name: string;
	full_name: string;
	nickname: string[];
	birth_place: string;
	birth_date: string;
	generation: string;
	introduction_phrase: string;
	profile_picture_url: string;
	join_details_jkt48?: string;
	promoted_details_jkt48?: string;
	previous_formation?: string;
	sub_unit?: string;
	fanbase_name?: string;
	reference?: string;
	social_media?: { [key: string]: string };
};

export const load = async ({
	params,
	fetch
}: {
	params: { id: string };
	fetch: typeof window.fetch;
}) => {
	const { id } = params;

	const response = await fetch(`/jkt48_members.json`);
	const data = await response.json();

	const member: Member = data.find((member: Member) => member.id === id);

	return {
		id,
		member
	};
};
