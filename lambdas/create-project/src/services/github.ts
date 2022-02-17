import { Octokit } from "octokit";

import { eventRequest } from "../models/schema";
import { parseDescription, parseTeamSlug } from "./parsers";

// * INFO: Creating a global instance for Octokit
const githubAPI = Octokit.defaults({
  auth: process.env.GITHUB_PAT!,
});

// * INFO: The default discussion template when a new team is created
const discussionTemplate = `
### **Maintainers are requested to only use 'Private Discussions' for conversations between them and contributors. This ensures privacy from other teams.**
#### **Video Demo:**
![Video Demo](https://imgur.com/ew6K6X2.gif)

#### **Before posting the discussion, make sure to select the 'Private' option below the text editor:**
![Select Option](https://imgur.com/34GAcqX.png)

#### **After you have posted, there must be be a lock icon on top-left of the discussion post:**
![Lock Icon](https://imgur.com/mT89Vll.png)

**Regards,**
**GitHub Community SRM**
`;

/**
 * Checks if a team exists or not, and returns it's ID
 * @param {string} team The team name
 * @returns {Promise<number>} The team ID
 */
export const checkTeamExists = async (team: string): Promise<number> => {
  try {
    const octokit = new githubAPI();
    const { data } = await octokit.request(
      "GET /orgs/{org}/teams/{team_slug}",
      {
        org: process.env.GITHUB_ORG!,
        team_slug: team,
      }
    );
    return data.id;
  } catch (err) {
    if (
      err.name &&
      err.status &&
      err.name === "HttpError" &&
      err.status === 404
    ) {
      return -1;
    } else {
      throw err;
    }
  }
};

/**
 * The function creates a year-wise team (of the format `AY2021-22`), if it does not exist
 * @param {string} team The year-name slug for the team name. Example: `AYXXXX-ZZ`
 * @returns {Promise<number>} The created team ID
 */
export const createParentTeam = async (team: string): Promise<number> => {
  const octokit = new githubAPI();
  const { data } = await octokit.request("POST /orgs/{org}/teams", {
    org: process.env.GITHUB_ORG!,
    name: team,
    privacy: "closed",
  });
  return data.id;
};

/**
 * Function creates a child team with all the approved maintainers
 * @param {eventRequest} event The lambda event invoked
 * @param {string} teamSlug The unique team slug created
 * @param {number} parentID The year-name (`AYXXXX-ZZ`) team ID
 * @param {string} parentSlug The year-name (`AYXXXX-ZZ`)
 * @returns
 */
export const createChildTeam = async (
  event: eventRequest,
  teamSlug: string,
  parentID: number,
  parentSlug: string
): Promise<{ slug: string }> => {
  const octokit = new githubAPI();
  // * INFO: Creating the child team with the unique team-slug
  const { data } = await octokit.request("POST /orgs/{org}/teams", {
    org: process.env.GITHUB_ORG!,
    name: teamSlug,
    privacy: "closed",
    description: event["project-name"],
    parent_team_id: parentID,
  });
  const teamID = data.id;
  const teamGenSlug = data.slug;
  const orgID = data.organization.id;
  // * INFO: Sending a welcome discussion to the new team, with instructions
  await octokit.request(
    "POST /organizations/{org_id}/team/{team_id}/discussions",
    {
      org_id: orgID,
      team_id: teamID,
      title: "Instructions on creating private discussions:",
      body: discussionTemplate,
      private: true,
    }
  );
  // * INFO: Iterating over the maintainer array, sending team invitation to each and adding them to internal maintainers team
  for (const [index, maintainer] of event.maintainers.entries()) {
    await octokit.request(
      "PUT /organizations/{org_id}/team/{team_id}/memberships/{username}",
      {
        org_id: orgID,
        team_id: teamID,
        username: maintainer,
        role: "maintainer",
      }
    );
    await octokit.request(
      "PUT /orgs/{org}/teams/{team_slug}/memberships/{username}",
      {
        org: process.env.GITHUB_ORG!,
        team_slug: "maintainers",
        username: maintainer,
        role: "member",
      }
    );
  }
  // * INFO: Returning a slug in the form of `AYXXXX-ZZ/abcd-efgh-1234:::12345/90876`
  return {
    slug: `${parentSlug}/${teamGenSlug}:::${orgID}/${teamID}`,
  };
};

/**
 * Function creates an empty repository and assigns the team appropriate permissions
 * @param {eventRequest} event The lambda event invoked
 * @param {string} slug The unique team-slug in the form of `AYXXXX-ZZ/abcd-efgh-1234:::12345/90876`
 * @returns {Promise<{link: string; slug: string;}>} Returns the created repository link and visibility status
 */
export const createEmptyRepository = async (
  event: eventRequest,
  slug: string
): Promise<{ link: string; private: boolean }> => {
  const teamInfo = parseTeamSlug(slug);
  const octokit = new githubAPI();
  // * INFO: Creating the empty repository under the team
  const { data } = await octokit.request("POST /orgs/{org}/repos", {
    org: process.env.GITHUB_ORG!,
    name: teamInfo["team-slug"],
    description: parseDescription(event["project-description"]),
    private: event.private,
    team_id: teamInfo["team-id"],
    auto_init: true,
  });
  // * INFO: Giving the team admin access to that repository
  await octokit.request(
    "PUT /orgs/{org}/teams/{team_slug}/repos/{owner}/{repo}",
    {
      org: process.env.GITHUB_ORG!,
      team_slug: teamInfo["team-slug"],
      owner: process.env.GITHUB_ORG!,
      repo: data.name,
      permission: "admin",
    }
  );
  return {
    link: data.html_url,
    private: data.private,
  };
};
