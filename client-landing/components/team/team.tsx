import { Member } from ".";
import { MemberProps } from "../../utils/interfaces";

interface TeamProps {
  team: MemberProps[];
}

const Team = ({ team }: TeamProps) => {
  return (
    <div>
      <div>
        <h1 className="text-center text-3xl lg:text-5xl font-bold mb-10 text-base-black">
          Admins
        </h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 text-center">
          {team?.map((member) => (
            <Member key={member.id} member={member} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Team;
