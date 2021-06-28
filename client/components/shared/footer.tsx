import { GitHubIcon, TwitterIcon, InstagramIcon } from "../../utils/icons";

const Footer = () => {
  const socials: {
    icon: JSX.Element;
    href: string;
  }[] = [
    {
      icon: <GitHubIcon />,
      href: "https://github.com",
    },
    {
      icon: <GitHubIcon />,
      href: "https://github.com",
    },
    {
      icon: <GitHubIcon />,
      href: "https://github.com",
    },
  ];

  return (
    <div className="bg-base-smoke flex flex-col md:flex-row justify-evenly items-center rounded-b-2xl p-2 md:p-6 text-white">
      <div className="w-1/3 h-0 md:h-auto"></div>
      <p className="w-full md:w-1/3 text-center my-2 md:my-auto text-black mx-2 min-w-max">
        Something Witty
      </p>
      <div className="w-full md:w-1/3 flex flex-row justify-around md:justify-evenly items-center">
        {socials.map((social) => (
          <a
            key={social.href}
            href={social.href}
            target="_blank"
            rel="noopener noreferrer"
            className="bg-base-teal flex justify-center items-center p-2 rounded-xl"
          >
            <span className="w-5 h-5">{social.icon}</span>
          </a>
        ))}
      </div>
    </div>
  );
};

export default Footer;
