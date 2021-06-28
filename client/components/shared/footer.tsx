import { GitHubIcon, TwitterIcon, InstagramIcon } from "../../utils/icons";

export default function Footer() {
  const Socials = [<GitHubIcon />, <TwitterIcon />, <InstagramIcon />];
  return (
    <div className="bg-base-blue flex flex-row justify-evenly rounded-b-2xl  p-4 md:p-6 text-white">
      <div className="w-1/3"></div>
      <p className="w-1/3 text-center my-auto">Something witty</p>
      <div className="w-1/3 flex flex-row justify-evenly items-center">
        {Socials.map((icon) => (
          <div className="bg-base-black flex justify-center items-center p-4 rounded-2xl">
            <div className="w-4 h-4">{icon}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
