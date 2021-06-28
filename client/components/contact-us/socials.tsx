import { GitHubIcon, LinkedinIcon, TwitterIcon } from "../../utils/icons";

const Left = () => {
  return (
    <section className="w-full max-w-2xl px-6 py-4 mx-auto bg-white  ">
      <h2 className="text-3xl font-semibold text-center text-gray-800 ">
        Get in touch
      </h2>
      <p className="mt-3 text-center text-gray-600 ">
        Lorem ipsum dolor sit amet consectetur, adipisicing elit.
      </p>
      <div className="flex justify-center">
        <div className="grid grid-cols-1 w-1/3  gap-10 mt-6 sm:grid-cols-2 md:grid-cols-2">
          <GitHubIcon />
          <LinkedinIcon />
          <TwitterIcon />
          <GitHubIcon />
        </div>
      </div>
    </section>
  );
};

export default Left;
