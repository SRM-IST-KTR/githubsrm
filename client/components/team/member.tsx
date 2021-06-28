import Socials from "./socials";
import { motion } from "framer-motion";

import { MemberProps } from "./../../utils/interfaces";

interface MemberProp {
  member: MemberProps;
}

const Profile = ({ member }: MemberProp) => {
  const holder = {
    initial: { scale: 1 },
    hover: { scale: 1.1 },
  };
  const img = {
    initial: { scale: 1 },
    hover: { scale: 0.8 },
  };

  const handles = [
    { github_id: member.github_id },
    { linkedin: member.linkedin },
    { twitter: member.twitter },
    { portfolio: member.portfolio },
  ];

  return (
    <div className="flex flex-col items-center m-4">
      <motion.div
        variants={holder}
        whileHover="hover"
        className="flex justify-center items-center rounded-full transform border-2 hover:border-base-teal hover:border-4 border-black p-4 relative"
      >
        <motion.img
          variants={img}
          alt={member.name}
          className="rounded-full relative w-48 h-48 object-cover z-10 "
          src={member.img_url}
        />
        <Socials handles={handles} />
      </motion.div>
      <h5 className="text-lg mt-6 font-medium">{member.name}</h5>
      <p className="text-sm">{`"${member.tagline}"`}</p>
    </div>
  );
};

export default Profile;
