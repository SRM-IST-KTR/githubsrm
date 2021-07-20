interface SectionProps {
  name: string;
  description: string;
  isActive: boolean;
  onError: boolean;
  setActive: () => void;
  icon: JSX.Element;
}

const Section = ({
  name,
  description,
  isActive,
  icon,
  setActive,
  onError,
}: SectionProps) => {
  return (
    <div onClick={setActive} className="flex w-full mx-1 lg:mb-10 lg:last:mb-0">
      <div
        className={`${
          onError
            ? "border-red-500"
            : isActive
            ? "border-base-green"
            : "border-transparent"
        } border-b-4 lg:border-b-0 lg:border-r-4 w-full cursor-pointer py-4 flex flex-col-reverse lg:flex-row items-start lg:items-center justify-between transform lg:hover:translate-y-0 lg:hover:-translate-x-4`}
      >
        <div className="h-full mt-2">
          <h3
            className={`${
              isActive ? "font-medium" : ""
            } lg:text-xl font-medium mb-2 min-w-max`}
          >
            {name}
          </h3>
          <p className="text-sm lg:text-sm w-full">{description}</p>
        </div>

        <div className="mx-auto lg:mx-4">
          <span
            className={`${
              onError
                ? "bg-red-500"
                : isActive
                ? "bg-base-green bg-opacity-80"
                : "bg-base-smoke"
            } w-8 lg:w-12 flex justify-center items-center p-1 lg:p-2 rounded-full`}
          >
            {icon}
          </span>
        </div>
      </div>
    </div>
  );
};

export default Section;
