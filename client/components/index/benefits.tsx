import { PuzzleIcon, CelebrationIcon, TickMark } from "../../utils/icons";

const Benefits = () => {
  const domainData: Array<{
    icon: JSX.Element;
    title: string;
    text: string;
  }> = [
    {
      icon: <PuzzleIcon />,
      title: "Contribution",
      text:
        "Students can contribute to Open Source Projects under the banner of SRMIST allowing students to get industry-level exposure through SRMIST’s organization.",
    },
    {
      icon: <TickMark />,
      title: "Eligibility",
      text:
        "Eligibility to apply for the GitHub Externship Program where one can solve real-world tech problems by collaborating on open source projects.",
    },
    {
      icon: <CelebrationIcon />,
      title: "Features",
      text:
        "Free access to GitHub Enterprise Server and GitHub Enterprise Cloud for every department and Exclusive access to new features, and GitHub Education-specific swag.",
    },
  ];

  return (
    <div className="flex flex-col justify-center lg:my-20">
      <h2 className="text-2xl lg:text-4xl lg:text-center font-extrabold text-base-black my-4">
        SRMIST is now a<br />
        <span className="text-base-blue">GitHub Campus Partner School</span>
      </h2>

      <figure className="my-2 lg:my-7 flex justify-center">
        <img
          draggable="false"
          src="/map.png"
          alt="github campus map"
          className="rounded-lg shadow-xl"
        />
      </figure>

      <div className="mt-14 flex justify-center">
        <h2 className="text-2xl lg:text-4xl text-base-teal font-extrabold">
          Benefits
        </h2>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 lg:gap-10 lg:mt-10 items-start">
        {domainData.map((data) => (
          <div
            key={data.title}
            className="flex flex-col lg:justify-center lg:items-center rounded-xl text-justify"
          >
            <div className="mt-6 lg:mt-0 mb-2 w-8 mx-auto flex justify-center items-center">
              {data.icon}
            </div>
            <h3 className="font-medium text-center lg:text-lg mb-2">
              {data.title}
            </h3>
            <p className="text-gray-600 font-regular text-sm lg:text-lg">
              {data.text}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Benefits;
