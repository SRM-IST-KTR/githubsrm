import Link from "next/link";

const Navbar = () => {
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
  ];

  return (
    <nav className="sticky top-0 w-full z-0 bg-base-black rounded-t-2xl shadow-lg">
      <ul className="flex z-40 font-semibold text-lg text-white mx-14 my-8">
        {links.map((link) => (
          <li
            key={link.href}
            className="mx-8 border-base-green transform hover:border-b-2"
          >
            <Link href={link.href}>
              <a className="relative py-2 px-4 text-xl transition-all duration-500 hover:text-base-green hover:z-1 underline-animation">
                {link.name}
              </a>
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default Navbar;
