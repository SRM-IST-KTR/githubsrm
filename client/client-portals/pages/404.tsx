import router from "next/router";
import { Layout } from "@/shared/index";
import { ErrorPage } from "@/icons/index";

const NotFound = () => {
  return (
    <Layout type="admin">
      <div className="flex flex-col justify-center items-center h-full md:mt-24 text-center">
        <h1 className="text-white text-9xl font-extrabold flex-nowrap flex my-1 py-2 px-5">
          4
          <span className="text-9xl animate-bounce">
            <ErrorPage />
          </span>
          4
        </h1>
        <h2 className="text-6xl text-white my-2 font-extrabold">Not Found</h2>
        <p className="flex flex-col text-xl lg:text-4xl text-white mt-16 font-semibold">
          <span>Seems like you're lost,</span>
          <span>
            let's get you{" "}
            <button
              className="text-white bg-base-teal md:p-3 py-3 md:min-w-32 min-w-24 font-semibold rounded-lg my-3"
              onClick={() => router.push("/")}
            >
              Home
            </button>
          </span>
        </p>
      </div>
    </Layout>
  );
};

export default NotFound;
