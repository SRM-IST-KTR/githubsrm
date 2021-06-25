import Socials from "./socials";
import { motion, useElementScroll, useTransform } from "framer-motion";

import { MemberProps } from "./../../utils/interfaces";

interface MemberProp {
  member: MemberProps;
}

const Profile = ({ member }: MemberProp) => {
  const holder = {
    initial: { scale: 1 },
    hover: { scale: 1.05 },
  };
  const img = {
    initial: { scale: 1 },
    hover: { scale: 0.8 },
  };

  return (
    <div className="flex flex-col items-center m-4">
      <motion.div
        variants={holder}
        whileHover="hover"
        className="rounded-full ring-2 ring-black p-4 relative"
      >
        <motion.img
          variants={img}
          alt={member.name}
          className="rounded-full relative w-48 h-48 object-cover z-10"
          src={member.img_url}
        />
        <Socials handles={member.handles} />
      </motion.div>
      <div className="text-lg font-montserrat my-2 font-normal">
        {member.name}
      </div>
      <div className="text-lg font-montserrat font-extralight">
        {`"${member.tagline}"`}
      </div>
    </div>
  );
};

export default Profile;
