import { Member } from "./";
import { MemberProps } from "./../../utils/interfaces";

const Team = () => {
  const members: MemberProps[] = [
    {
      name: "Abhishek Saxena",
      gitHub_id: "URL",
      handles: [
        { linkedin: "aasa" },
        { github: "fakegithub" },
        { portfolio: "something" },
      ],
      img_url: "./test.webp",
      tagline: "line1",
    },
    {
      name: " sakshi",
      gitHub_id: "URL",
      handles: [{ linkedin: "aasa" }, { portfolio: "something" }],
      img_url: "./test2.webp",
      tagline: "line2",
    },
  ];

  return (
    <div className="flex flex-wrap">
      {members.map((member) => (
        <Member key={member.gitHub_id} member={member} />
      ))}
    </div>
  );
};

export default Team;
