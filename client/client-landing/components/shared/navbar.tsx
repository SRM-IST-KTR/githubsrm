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
      name: "Documentation",
      href: "/documentation",
    },
    {
      name: "Contact Us",
      href: "/contact-us",
    },
  ];

  return (
    <nav className="mb-4 bg-base-black rounded-lg custom-scrollbar overflow-auto overflow-y-hidden py-2 px-4">
      <ul className="grid grid-flow-col auto-cols-auto text-white my-2 lg:my-8 w-full lg:w-6/12 text-center">
        {links.map((link) => (
          <li
            key={link.href}
            className={`${
              asPath === link.href ? "font-semibold" : ""
            } min-w-max transform hover:-translate-y-1 cursor-pointer mb-2`}
          >
            <Link href={link.href}>
              <a className="lg:my-2 lg:text-xl px-6">{link.name}</a>
            </Link>
          </li>
        ))}
        <li className="w-1/5"></li>
      </ul>
    </nav>
  );
};

export default Navbar;
