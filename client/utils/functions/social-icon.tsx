import { LinkedinIcon, GitHubIcon, TwitterIcon, GlobeIcon } from "../icons";

interface SocialIconProps {
  handle: { [handle: string]: string };
}

export const SocialIcon = ({ handle }: SocialIconProps): JSX.Element => {
  if (handle["linkedin"]) {
    return (
      <a target="_blank" rel="noopener noreferrer" href={handle["linkedin"]}>
        <LinkedinIcon />
      </a>
    );
  }
  if (handle["github_id"]) {
    return (
      <a target="_blank" rel="noopener noreferrer" href={handle["github_id"]}>
        <GitHubIcon />
      </a>
    );
  }
  if (handle["portfolio"]) {
    return (
      <a target="_blank" rel="noopener noreferrer" href={handle["portfolio"]}>
        <GlobeIcon />
      </a>
    );
  }
  if (handle["twitter"]) {
    return (
      <a target="_blank" rel="noopener noreferrer" href={handle["twitter"]}>
        <TwitterIcon />
      </a>
    );
  }

  return <></>;
};
