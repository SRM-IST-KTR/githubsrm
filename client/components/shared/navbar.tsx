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
  ];

  return (
    <nav className="sticky top-0 w-full z-0 mb-4 bg-base-black rounded-2xl shadow-lg">
      <ul className="flex justify-between z-40 text-white mx-10 my-8 w-6/12 text-center">
        {links.map((link) => (
          <li
            key={link.href}
            className={`${
              asPath === link.href ? "font-semibold" : ""
            } w-full transform hover:-translate-y-1`}
          >
            <Link href={link.href}>
              <a className="my-2 text-xl">{link.name}</a>
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default Navbar;
