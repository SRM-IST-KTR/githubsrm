import { Member } from "./";
import { MemberProps } from "./../../utils/interfaces";

const Team = () => {
  const members: MemberProps[] = [
    {
      name: "Abhishek Saxena",
      gitHub_id: "URL",
      handles: [{ linkedin: "aasa" }],
      img_url: "./test.webp",
      tagline: "line1",
    },
    {
      name: " sakshi",
      gitHub_id: "URL",
      handles: [{ linkedin: "aasa" }],
      img_url: "./test2.webp",
      tagline: "line2",
    },
  ];

  return (
    <div>
      {members.map((member) => (
        <Member key={user.gitHub_id} member={member} />
      ))}
    </div>
  );
};

export default Team;
