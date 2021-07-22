import {
  GithubIcon,
  TwitterIcon,
  InstagramIcon,
  LinkedinIcon,
} from "@/icons/index";

const Footer = () => {
  const socials: {
    icon: JSX.Element;
    href: string;
    name: string;
  }[] = [
    {
      name: "Github",
      icon: <GithubIcon />,
      href: "https://github.com/srm-ist-ktr",
    },
    {
      name: "Twitter",
      icon: <TwitterIcon />,
      href: "https://twitter.com/githubsrm",
    },
    {
      name: "Linkedin",
      icon: <LinkedinIcon />,
      href: "https://www.linkedin.com/company/githubsrm/mycompany/",
    },
    {
      name: "Instagram",
      icon: <InstagramIcon />,
      href: "https://www.instagram.com/githubsrm/",
    },
  ];

  return (
    <footer className="bg-base-smoke flex flex-col lg:flex-row justify-evenly items-center px-2 py-4 lg:p-6 text-white">
      <div className="hidden lg:flex lg:w-1/3 h-auto my-4 mx-2 text-center text-base-blue font-medium">
        <a href="mailto:community@githubsrm.tech">community@githubsrm.tech</a>
      </div>

      <p className="w-full lg:w-1/3 text-center my-4 lg:my-auto text-gray-700 font-regular mx-2 text-sm">
        Alone we can do so little, together we can do so much.
        <br />
        <strong>GitHub Community SRM</strong>
      </p>

      <div className="w-full lg:hidden h-auto mb-4 mx-2 text-center text-base-blue font-medium">
        <a href="mailto:community@githubsrm.tech">community@githubsrm.tech</a>
      </div>

      <div className="w-full lg:w-1/3 flex justify-evenly items-center">
        {socials.map((social) => (
          <div key={social.href}>
            <a
              aria-label={social.name}
              href={social.href}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-base-teal flex justify-center items-center p-2 rounded-xl mx-auto"
            >
              <span className="w-5 h-5">{social.icon}</span>
            </a>
          </div>
        ))}
      </div>
    </footer>
  );
};

export default Footer;
