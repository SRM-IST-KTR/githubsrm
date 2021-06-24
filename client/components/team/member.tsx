import Socials from "./socials";
import { motion, useElementScroll, useTransform } from "framer-motion";

import { MemberProps } from "./../../utils/interfaces";

interface MemberProp {
  member: MemberProps;
}

const Profile = ({ member }: MemberProp) => {
  return (
    <div className="flex flex-wrap">
      <div className="flex flex-col items-center m-4">
        <div className="rounded-full ring-2 ring-black p-4">
          <Socials handles={member.handles} />
          <img
            alt={member.name}
            className="rounded-full w-48 h-48 object-cover"
            src={member.img_url}
          />
        </div>
        <div className="text-lg font-montserrat font-normal">{member.name}</div>
        <div className="text-lg font-montserrat font-extralight">
          {`"${member.tagline}"`}
        </div>
      </div>
    </div>
  );
};

export default Profile;
