import { OtherMaintainersProps } from "utils/interfaces";

interface otherMaintainersProps {
  otherMaintainers: OtherMaintainersProps[];
}

const OtherMaintainers = ({ otherMaintainers }: otherMaintainersProps) => {
  return (
    <div className="my-10 flex">
      <h1 className="text-gray-200 font-medium text-xl flex mr-3">
        {otherMaintainers?.length > 0
          ? "Other Maintainers :"
          : "There are no other maintainers in this project"}
      </h1>

      {otherMaintainers?.length > 0 &&
        otherMaintainers?.map((maintainer) => (
          <p
            key={maintainer.github}
            className="text-2xl cursor-pointer text-gray-100 "
          >
            <a
              target="_blank"
              rel="noopener noreferrer"
              href={maintainer.github}
              className="hover:text-gray-600"
            >
              {maintainer.name}
            </a>
          </p>
        ))}
    </div>
  );
};

export default OtherMaintainers;
