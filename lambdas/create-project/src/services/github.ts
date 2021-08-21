import { Octokit } from "octokit";

import { eventRequest } from "../models/schema";

const githubAPI = Octokit.defaults({
  auth: process.env.GITHUB_PAT!,
});

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

export const createParentTeam = async (team: string): Promise<number> => {
  const octokit = new githubAPI();
  const { data } = await octokit.request("POST /orgs/{org}/teams", {
    org: process.env.GITHUB_ORG!,
    name: team,
    privacy: "closed",
  });
  return data.id;
};

export const createChildTeam = async (
  event: eventRequest,
  teamSlug: string,
  parentID: number,
  parentSlug: string
): Promise<{ slug: string; id: number }> => {
  const octokit = new githubAPI();
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
  for (const [index, maintainer] of event.maintainers.entries()) {
    await octokit.request(
      "PUT /orgs/{org}/teams/{team_slug}/memberships/{username}",
      {
        org: process.env.GITHUB_ORG!,
        team_slug: teamGenSlug,
        username: maintainer,
        role: "maintainer",
      }
    );
  }
  return {
    slug: `${parentSlug}/${teamGenSlug}`,
    id: teamID,
  };
};
