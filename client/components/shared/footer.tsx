import { GitHubIcon, TwitterIcon, InstagramIcon } from "../../utils/icons";

export default function Footer() {
  const Socials = [<GitHubIcon />, <TwitterIcon />, <InstagramIcon />];
  return (
    <div className="bg-base-smoke flex flex-col md:flex-row justify-evenly items-center rounded-b-2xl  p-4 md:p-6 text-white">
      <div className="w-1/3"></div>
      <p className="w-1/3 text-center my-auto text-black font-thin mx-2">
        Something Witty
      </p>
      <div className="w-1/3 flex flex-row justify-evenly items-center">
        {Socials.map((icon) => (
          <div className="bg-base-blue flex justify-center items-center p-2 rounded-xl">
            <div className="w-5 h-5">{icon}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
