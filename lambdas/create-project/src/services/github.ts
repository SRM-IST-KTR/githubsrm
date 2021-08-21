import { Octokit } from "octokit";

const githubAPI = Octokit.defaults({
  auth: process.env.GITHUB_PAT!,
});
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
