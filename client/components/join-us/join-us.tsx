import { useState } from "react";
import Link from "next/link";
import { ArrowIcon } from "../../utils/icons";

const test = () => {
  let [formOption, setFormOption] = useState(true);

  const href = ["/join-us/contributor", "/join-us/maintainer"];
  return (
    <>
      <h1 className="font-medium ml-16 text-5xl">Join us as a?</h1>
      <section className="flex flex-row h-full">
        <div className="w-1/3 p-4">
          <div className={`flex flex-col justify-evenly items-center`}>
            <span
              onClick={() => setFormOption(true)}
              className={` ${
                !formOption ? "text-xl" : "text-2xl text-base-green"
              } h-48 flex flex-row items-center cursor-pointer`}
            >
              Contributor
              {/* <div className="w-5 h-5">
                <ArrowIcon />
              </div> */}
            </span>
            <span
              onClick={() => setFormOption(false)}
              className={` ${
                formOption ? "text-xl" : "text-2xl text-base-green"
              } h-48 flex flex-row items-center cursor-pointer`}
            >
              Maintainer
              {/* <div className="w-5 h-5">
                <ArrowIcon />
              </div> */}
            </span>
          </div>
        </div>
        <div className=" w-full p-12 ">
          <div className=" p-8 bg-base-smoke border-t-4 rounded-sm border-base-green shadow-lg">
            {formOption ? (
              <>
                <h2 className="text-4xl mb-4">Your Job as a Contributor</h2>
                <p className="text-md">
                  Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae
                  dolores deserunt ea doloremque natus error, rerum quas quaerat
                  nam ex commodi hic, suscipit in a veritatis pariatur minus
                  consequuntur!
                </p>
              </>
            ) : (
              <>
                <h2 className="text-4xl mb-4">Your Job as a Maintainer</h2>
                <p className="text-md">
                  Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae
                  dolores deserunt ea doloremque natus error, rerum quas quaerat
                  nam ex commodi hic, suscipit in a veritatis pariatur minus
                  consequuntur!o
                </p>
              </>
            )}
          </div>
          <div className=" w-32 text-center text-white my-8 p-4 rounded-md hover:bg-base-blue bg-base-teal ml-auto mr-3">
            {formOption ? (
              <Link href={href[0]}>Contributor</Link>
            ) : (
              <Link href={href[1]}>Maintainer</Link>
            )}
          </div>
        </div>
      </section>
    </>
  );
};

export default test;
