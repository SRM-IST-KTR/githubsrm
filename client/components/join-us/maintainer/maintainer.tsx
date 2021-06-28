import Link from "next/link";

const Maintainer = () => {
  return (
    <div>
      <div>
        <div className="font-medium">
          <h1 className="text-4xl">Maintainer</h1>
          <h2 className="text-xl mt-2">descrip</h2>
        </div>

        <p className="text-right text-lg">
          Join us as a{" "}
          <Link href="/join-us/contributor">
            <a className="text-base-green font-bold hover:underline">
              Contributor
            </a>
          </Link>
        </p>
      </div>

      <div className="text-center">
        <p className="text-lg">please choose your bid</p>

        <div className="grid grid-cols-3 w-8/12 mx-auto mt-8">
          <Link href="/join-us/maintainer/new-project">
            <a className="bg-base-teal text-white rounded-lg text-xl py-4 font-medium">
              New Project
            </a>
          </Link>

          <span />

          <Link href="/join-us/maintainer/existing-project">
            <a className="bg-base-teal text-white rounded-lg text-xl py-4 font-medium">
              Existing Project
            </a>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Maintainer;
