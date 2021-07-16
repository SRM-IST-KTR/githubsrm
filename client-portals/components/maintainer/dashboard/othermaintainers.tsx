const OtherMaintainers = ({ otherMaintainers }) => {
  return (
    <div className="my-10">
      <h1 className="text-white font-bold text-xl">
        {otherMaintainers?.length > 0
          ? "Other Maintainers -"
          : "No other maintainers"}
      </h1>

      {otherMaintainers?.length > 0 &&
        otherMaintainers?.map((maintainer) => (
          <p
            key={maintainer.github}
            className="text-2xl cursor-pointer text-white list-disc"
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
