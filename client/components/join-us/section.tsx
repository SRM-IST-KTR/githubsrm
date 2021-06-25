interface SectionProps {
  name: string;
  isActive: boolean;
  onError: boolean;
  setActive: () => void;
}

const Section = ({ name, isActive, setActive, onError }: SectionProps) => {
  return (
    <div onClick={setActive} className="relative w-full m-8">
      {/* <div> */}
      <p className={`${!isActive ? "text-base-green" : ""} w-3/4 py-3`}>{name}</p>
      <span
        className={`${isActive ? "hidden" : ""} ${
          onError ? "bg-red-600" : "bg-base-green"
        } rounded-full w-5 h-5 absolute top-0 bottom-0`}
      />
      {/* </div> */}
    </div>
  );
};

export default Section;
