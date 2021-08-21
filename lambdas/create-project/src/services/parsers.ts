import { customAlphabet } from "nanoid";
import { lowercase, numbers } from "nanoid-dictionary";
import slugify from "slugify";

export const generateTeamID = async (team: string): Promise<string> => {
  const slug = slugify(team);
  const id_1 = customAlphabet(lowercase, 4)();
  const id_2 = customAlphabet(numbers, 4)();
  const id = [];
  for (const [index, char] of id_1.split("").entries()) {
    id.push(char);
    id.push(id_2.split("")[index]);
  }
  return `${slug}-${id.join("")}`;
};

export const generateYearID = async (year: string): Promise<string> => {
  const suffix = +year.slice(-2);
  return `AY${year}-${suffix + 1}`;
};

export const parseTeamSlug = (
  slug: string
): {
  "parent-slug": string;
  "team-slug": string;
  "org-id": number;
  "team-id": number;
} => {
  const slugPart = slug.split(":::")[0];
  const idPart = slug.split(":::")[1];
  return {
    "parent-slug": slugPart.split("/")[0],
    "team-slug": slugPart.split("/")[1],
    "org-id": +idPart.split("/")[0],
    "team-id": +idPart.split("/")[1],
  };
};
