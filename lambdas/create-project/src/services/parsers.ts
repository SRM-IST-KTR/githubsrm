import { customAlphabet } from "nanoid";
import { lowercase, numbers } from "nanoid-dictionary";
import slugify from "slugify";

/**
 * Function used to generate team unique slug
 * @param {string} team The team name fetched from the event
 * @returns {Promise<string>} The unique team-slug
 */
export const generateTeamID = async (team: string): Promise<string> => {
  let slug = slugify(team);
  const id_1 = customAlphabet(lowercase, 4)();
  const id_2 = customAlphabet(numbers, 4)();
  const id = [];
  for (const [index, char] of id_1.split("").entries()) {
    id.push(char);
    id.push(id_2.split("")[index]);
  }
  slug = slug.substring(0, 90);
  return `${slug}-${id.join("")}`;
};

/**
 * Generates a year-name slug, for example `AY2021-22`
 * @param {string} year The 4-digit year
 * @returns {Promise<string>} The year-name slug
 */
export const generateYearID = async (year: string): Promise<string> => {
  const suffix = +year.slice(-2);
  return `AY${year}-${suffix + 1}`;
};

/**
 * Parses the team-slug generated from the previous steps in the form of `AYXXXX-ZZ/abcd-efgh-1234:::12345/90876`
 * @param slug
 * @returns {{"parent-slug": string; "team-slug": string; "org-id": number; "team-id": number;}} The parsed data
 */
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

export const parseDescription = (description: string) => {
  description = description.replace(/\n/g, " ");
  return description;
};
