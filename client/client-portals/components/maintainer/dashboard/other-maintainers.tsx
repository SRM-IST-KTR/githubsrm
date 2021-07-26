import { OtherMaintainersProps } from "utils/interfaces";

interface otherMaintainersProps {
  otherMaintainers: OtherMaintainersProps[];
}

const OtherMaintainers = ({ otherMaintainers }: otherMaintainersProps) => {
  return (
    <div className="md:my-7 my-10 flex">
      <h1 className="text-gray-200 font-semibold text-2xl flex mr-3">
        {otherMaintainers?.length > 0
          ? "Other Maintainers :"
          : "There are no other maintainers in this project"}
      </h1>

      {otherMaintainers?.length > 0 &&
        otherMaintainers?.map((maintainer, index) => (
          <p
            key={maintainer.github}
            className="text-2xl cursor-pointer text-gray-100 "
          >
            <a
              target="_blank"
              rel="noopener noreferrer"
              href={maintainer.github}
              className="hover:text-base-green"
            >
              {maintainer.name}{" "}
              {index !== otherMaintainers?.length - 1 && (
                <span className="text-2xl">|&nbsp;</span>
              )}
            </a>
          </p>
        ))}
    </div>
  );
};

export default OtherMaintainers;
