import { FaGithub, FaInstagram, FaLinkedin, FaTwitter } from "react-icons/fa";

const Socials = () => {
  const socials: { href: string; icon: JSX.Element }[] = [
    {
      href: "https://github.com/srm-ist-ktr",
      icon: <FaGithub />,
    },
    {
      href: "https://www.linkedin.com/in/githubsrm",
      icon: <FaLinkedin />,
    },
    {
      href: "https://twitter.com/githubsrm",
      icon: <FaTwitter />,
    },
    {
      href: "https://www.instagram.com/githubsrm/",
      icon: <FaInstagram />,
    },
  ];

  return (
    <div className="flex">
      {socials.map((social) => (
        <a
          key={social.href}
          href={social.href}
          target="_blank"
          rel="noopener noreferrer"
          className="mx-4 text-3xl"
        >
          {social.icon}
        </a>
      ))}
    </div>
  );
};

export default Socials;
