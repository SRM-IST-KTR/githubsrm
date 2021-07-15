const OtherMaintainers = () => {
  const otherMaintainers = [
    {
      name: "Sebastian",
      github: "https://github.com/sebastian-bergmann",
    },
    {
      name: "Sebastian Bergmann",
      github: "https://github.com/sebastianbergmann",
    },
    {
      name: "Sebastian",
      github: "https://github.com/sebastian-bergmann",
    },
  ];

  return (
    <div>
      <h1 className="text-white font-extrabold text-3xl">Other Maintainers</h1>
      <ul>
        {otherMaintainers.map((maintainer) => (
          <li key={maintainer.name} className="text-2xl text-white list-disc">
            <a href={maintainer.github}>{maintainer.name}</a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default OtherMaintainers;
