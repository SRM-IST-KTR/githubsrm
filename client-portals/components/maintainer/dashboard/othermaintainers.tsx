import { OtherMaintainersProps } from "../../../utils/interfaces";

interface otherMaintainersProps {
  otherMaintainers: OtherMaintainersProps[];
}

const OtherMaintainers = ({ otherMaintainers }: otherMaintainersProps) => {
  return (
    <div className="my-10 flex justify-evenly">
      <h1 className="text-white font-bold text-xl flex">
        {otherMaintainers?.length > 0
          ? "Other Maintainers :"
          : "There are no other maintainers in this project"}
      </h1>
      <ul className="list-disc">
        {otherMaintainers?.length > 0 &&
          otherMaintainers?.map((maintainer) => (
            <li
              key={maintainer.github}
              className="text-2xl cursor-pointer text-white "
            >
              <a
                target="_blank"
                rel="noopener noreferrer"
                href={maintainer.github}
                className="hover:text-gray-600"
              >
                {maintainer.name}
              </a>
            </li>
          ))}
      </ul>
    </div>
  );
};

export default OtherMaintainers;
