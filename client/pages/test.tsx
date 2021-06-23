import { Hero } from "../components";

const IndexPage = () => {
  return (
    <div className="h-screen lg:px-7 lg:pt-14 px-5 pt-2">
      <div className="bg-baseBlack rounded-t-xl h-full overflow-auto p-5">
        {/*  TODO */}
        {/* navbar */}
        <header>
          <ul className="flex justify-evenly">
            <li>Head</li>
            <li>About</li>
            <li>Projects</li>
          </ul>
        </header>
        {/* navbar */}
        <h1 className="text-9xl text-center font-montserrat font-thin text-transparent bg-clip-text bg-gradient-to-b from-baseSmoke to-transparent">
          OSS
        </h1>
        <div className="bg-white rounded-md">main</div>
      </div>
    </div>
  );
};

export default IndexPage;
