import { Layout } from "@/shared/index";
import { ServerError } from "@/icons/index";
import router from "next/router";

const ServerErrorPage = () => {
  return (
    <>
      <Layout type="admin">
        <div className="flex flex-col justify-center items-center h-full md:mt-24 text-center">
          <h1 className="text-white text-9xl font-extrabold flex-nowrap flex my-1 py-2 px-5">
            5
            <span className="flex text-9xl animate-pulse">
              <ServerError />
              <ServerError />
            </span>
          </h1>
          <h2 className="text-5xl text-white my-2 font-extrabold">
            Oops! Something went wrong!
          </h2>
          <p className="text-xl lg:text-4xl text-white mt-16 font-semibold">
            Sorry, There was some issue on our end :(
          </p>
          <div>
            <button
              className="text-white text-3xl bg-base-teal md:p-3 p-2  min-w-32 font-semibold rounded-lg my-3 mx-2"
              onClick={() => router.push("https://githubsrm.tech/contact-us")}
            >
              Report this issue
            </button>
            <button
              className="text-white text-3xl bg-base-teal p-3 md:min-w-32 min-w-24 font-semibold rounded-lg my-3 mx-2"
              onClick={() => router.push("/")}
            >
              Home
            </button>
          </div>
        </div>
      </Layout>
    </>
  );
};

export default ServerErrorPage;
