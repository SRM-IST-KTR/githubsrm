import { useEffect, useState, useRef } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowIcon } from "../../utils/icons";

const test = () => {
  let [formOption, setFormOption] = useState(false);

  // //TODO: Put inside one object
  const list1 = ["Contributor", "Maintainer"];
  const href = ["/join-us/contributor", "/join-us/maintainer"];
  return (
    <>
      <h1 className="font-medium text-5xl">Join us as a?</h1>
      <section className="container flex flex-row items-stretch">
        <div className="w-1/3 p-4">
          <div
            className={`flex flex-col ${
              formOption ? "justify-start" : "justify-end"
            } items-center`}
          >
            <span
              onClick={() => setFormOption(true)}
              className={` ${
                !formOption ? "text-xl" : "text-4xl text-base-green"
              } h-36 flex flex-row items-center cursor-pointer`}
            >
              Contributor
              <div className="w-5 h-5">
                <ArrowIcon />
              </div>
            </span>
            <span
              onClick={() => setFormOption(false)}
              className={` ${
                formOption ? "text-xl" : "text-4xl text-base-green"
              } h-36 flex flex-row items-center cursor-pointer`}
            >
              Maintainer
              <div className="w-5 h-5">
                <ArrowIcon />
              </div>
            </span>
          </div>
        </div>
        <div className=" w-full h-auto p-12 ">
          <div className=" p-4 bg-base-smoke border-t-4 rounded-sm border-base-green shadow-lg h-full">
            {formOption ? (
              <>
                <h2 className="text-lg">Your Job as a Contributor</h2>
                <p>Stuff You would do</p>
              </>
            ) : (
              <>
                <h2 className="text-lg">Your Job as a Maintainer</h2>
                <p>Stuff You would do</p>
              </>
            )}
          </div>
          <div className=" w-32 text-center text-white mt-2 p-4 rounded-sm bg-base-teal ml-auto mr-3">
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
