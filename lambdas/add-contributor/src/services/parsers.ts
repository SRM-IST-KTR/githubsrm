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
