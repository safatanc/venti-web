import { readFileSync } from 'fs';
import path from 'path';
import type { PageServerLoad } from './$types';

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

export const load: PageServerLoad = async () => {
	const projectRoot = process.cwd();
	const filePath = path.join(projectRoot, 'static', 'jkt48_members.json');

	const fileContents = readFileSync(filePath, 'utf-8');
	const data: Member[] = JSON.parse(fileContents);

	return {
		members: data
	};
};
