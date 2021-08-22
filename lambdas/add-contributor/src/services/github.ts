import { Octokit } from "octokit";

import { eventRequest } from "../models/schema";
import { parseTeamSlug } from "./parsers";

// * INFO: Creating a global instance for Octokit
const githubAPI = Octokit.defaults({
  auth: process.env.GITHUB_PAT!,
});

/**
 * * INFO: The parsed data format after parsing the unique team-slug
 */
interface parsedData {
  "parent-slug": string;
  "team-slug": string;
  "org-id": number;
  "team-id": number;
}

/**
 * Function to add a contributor to a team
 * @param {parsedData} data The parsed data from the unique team-slug
 * @param {string} contributor The contributor GitHub ID
 */
export const addContributor = async (data: parsedData, contributor: string) => {
  const octokit = new githubAPI();
  await octokit.request(
    "PUT /organizations/{org_id}/team/{team_id}/memberships/{username}",
    {
      org_id: data["org-id"],
      team_id: data["team-id"],
      username: contributor,
      role: "member",
    }
  );
};
