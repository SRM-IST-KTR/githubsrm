import { useState } from "react";
import Link from "next/link";
import { ArrowIcon } from "../../utils/icons";

const JoinUs = () => {
  let [isContributor, setIsContributor] = useState<boolean>(true);

  const roles: {
    name: string;
    href: string;
    statement: string;
    description: string;
    icon: JSX.Element;
    isContributor: boolean;
  }[] = [
    {
      name: "Contributor",
      href: "/join-us/contributor",
      statement: "mini desc",
      description:
        " Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat am ex commodi hic, suscipit in a veritatis pariatur minus               consequuntur!",
      icon: <ArrowIcon />,
      isContributor: true,
    },
    {
      name: "Maintainer",
      href: "/join-us/maintainer",
      statement: "mini desc",
      description:
        " Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat am ex commodi hic, suscipit in a veritatis pariatur minus               consequuntur!",
      icon: <ArrowIcon />,
      isContributor: false,
    },
  ];

  return (
    <div>
      <div className="font-medium">
        <h1 className="text-4xl">There are 2</h1>
        <h2 className="text-xl mt-2">small text here</h2>
      </div>

      <div className="flex justify-evenly mt-8">
        <div className="w-4/12 flex flex-col items-center justify-between border-r-2">
          {roles.map((role) => (
            <div className="flex w-full">
              <div
                onClick={() => setIsContributor(role.isContributor)}
                className={`${
                  isContributor === role.isContributor
                    ? "border-base-green"
                    : "border-transparent"
                } border-r-4 w-full cursor-pointer py-4 flex items-center justify-between transform hover:-translate-x-4`}
              >
                <div>
                  <h3
                    className={`${
                      isContributor === role.isContributor ? "font-medium" : ""
                    } text-xl mb-2`}
                  >
                    {role.name}
                  </h3>
                  <p className="text-sm w-full">{role.statement}</p>
                </div>

                <div className="mx-4">
                  <span
                    className={`${
                      isContributor === role.isContributor
                        ? "bg-base-green bg-opacity-80"
                        : "bg-base-smoke"
                    } w-12 flex justify-center items-center p-2 rounded-full`}
                  >
                    {role.icon}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="w-full px-8">
          <div className="p-8 bg-gray-100 border-t-8 rounded-sm border-base-green">
            {roles.map((role) => (
              <>
                {role.isContributor === isContributor && (
                  <div>
                    <h2 className="text-4xl mb-4">
                      Your Job as a <strong>{role.name}</strong>
                    </h2>
                    <p className="text-md">{role.description}</p>

                    <div className="grid grid-cols-3 gap-x-16 items-center justify-center mt-10">
                      <span />
                      <span />
                      <Link href={role.href}>
                        <a className="text-white bg-base-green py-3 font-semibold rounded-lg text-center">
                          Apply Now!
                        </a>
                      </Link>
                    </div>
                  </div>
                )}
              </>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default JoinUs;
