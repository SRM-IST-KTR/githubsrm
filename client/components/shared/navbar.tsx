import Link from "next/link";
import { useRouter } from "next/router";

const Navbar = () => {
  const { asPath } = useRouter();

  const links: { name: string; href: string }[] = [
    {
      name: "Home",
      href: "/",
    },
    {
      name: "Projects",
      href: "/projects",
    },
    {
      name: "Team",
      href: "/team",
    },
    {
      name: "Join Us",
      href: "/join-us",
    },
    {
      name: "Contact Us",
      href: "/contact-us",
    },
  ];

  return (
    <nav className="h-fit-content w-full z-0 mb-4 bg-base-black rounded-2xl shadow-inner  overflow-y-hidden">
      <ul className="grid grid-flow-col auto-cols-auto text-white mx-8 lg:mx-10 my-2 lg:my-8 w-full lg:w-6/12 text-center">
        {links.map((link) => (
          <li
            key={link.href}
            className={`${
              asPath === link.href ? "font-semibold" : ""
            } min-w-max mx-4 transform hover:-translate-y-1 cursor-pointer`}
          >
            <Link href={link.href}>
              <span className="lg:my-2 lg:text-xl">{link.name}</span>
            </Link>
          </li>
        ))}
        <li className="w-1/5"></li>
      </ul>
    </nav>
  );
};

export default Navbar;
