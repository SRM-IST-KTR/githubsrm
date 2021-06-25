import { LinkedinIcon, GitHubIcon, TwitterIcon, GlobeIcon } from "../icons";

interface SocialIconProps {
  handles: { [handle: string]: string };
}

export const SocialIcon = ({ handles }: SocialIconProps): JSX.Element => {
  if (handles["linkedin"]) {
    return (
      <a target="_blank" rel="noopener noreferrer" href={handles["linkedin"]}>
        <LinkedinIcon />
      </a>
    );
  }
  if (handles["github"]) {
    return (
      <a target="_blank" rel="noopener noreferrer" href={handles["github"]}>
        <GitHubIcon />
      </a>
    );
  }
  if (handles["portfolio"]) {
    return (
      <a target="_blank" rel="noopener noreferrer" href={handles["portfolio"]}>
        <GlobeIcon />
      </a>
    );
  }
  if (handles["twitter"]) {
    return (
      <a target="_blank" rel="noopener noreferrer" href={handles["twitter"]}>
        <TwitterIcon />
      </a>
    );
  }
};

export default SocialIcon;
