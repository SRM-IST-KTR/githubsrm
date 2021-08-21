import { customAlphabet } from "nanoid";
import { lowercase, numbers } from "nanoid-dictionary";
import slugify from "slugify";

export const generateTeamID = async (team: string): Promise<string> => {
  const slug = slugify(team);
  const id_1 = customAlphabet(lowercase, 4);
  const id_2 = customAlphabet(numbers, 4);
  return `${slug}-${id_1}-${id_2}`;
};

export const generateYearID = async (year: string): Promise<string> => {
  const suffix = +year.slice(-2);
  return `AY${year}-${suffix + 1}`;
};
