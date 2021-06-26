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
    <div onClick={setActive} className="flex w-full mb-10 last:mb-0">
      <div
        className={`${
          onError
            ? "border-red-500"
            : isActive
            ? "border-base-green"
            : "border-transparent"
        } border-r-4 w-full cursor-pointer py-4 flex items-center justify-between transform hover:-translate-x-4`}
      >
        <div className="">
          <h3 className={`${isActive ? "font-medium" : ""} text-xl mb-2`}>
            {name}
          </h3>
          <p className="text-sm w-full">{description}</p>
        </div>

        <div className="mx-4">
          <span
            className={`${
              onError
                ? "bg-red-500"
                : isActive
                ? "bg-base-green bg-opacity-80"
                : "bg-base-smoke"
            } w-12 flex justify-center items-center p-2 rounded-full`}
          >
            {icon}
          </span>
        </div>
      </div>
    </div>
  );
};

export default Section;
