interface linkProps {
  fnc: Function;
  sources: {
    href: string;
    name: string;
  }[];
  current: string;
  icon: JSX.Element;
}

const PdfSideBarLink = ({ fnc, sources, current, icon }: linkProps) => {
  return (
    <>
      <p className="text-3xl my-3">PDF Tutorial</p>
      {sources.map((source) => (
        <div key={source.name} className="flex mx-2 w-full">
          <div
            onClick={() => fnc({ source: source, type: "PDF" })}
            className={`${
              current === source.href
                ? "border-base-green"
                : "md:border-transparent"
            } border-b-4 md:border-b-0 md:border-r-4 w-full cursor-pointer py-4 flex items-center justify-between transform hover:md:-translate-x-4`}
          >
            <div>
              <h3
                className={`${
                  current === source.href ? "font-medium" : ""
                } text-xl mb-2`}
              >
                {source.name}
              </h3>
            </div>

            <div className="mx-4">
              <span
                className={`${
                  current === source.href
                    ? "bg-base-green bg-opacity-80"
                    : "bg-base-smoke"
                } w-12 hidden md:flex justify-center items-center p-2 rounded-full`}
              >
                {icon}
              </span>
            </div>
          </div>
        </div>
      ))}
    </>
  );
};

export default PdfSideBarLink;
