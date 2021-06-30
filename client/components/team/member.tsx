import Socials from "./socials";
import { motion } from "framer-motion";
import { MemberProps } from "./../../utils/interfaces";

interface MemberProp {
  member: MemberProps;
}

const Profile = ({ member }: MemberProp) => {
  const holder = {
    initial: () => {
      if (window.innerWidth < 786) {
        return { scale: 1.1 };
      } else {
        return { scale: 1 };
      }
    },
    hover: { scale: 1.1 },
  };
  const img = {
    initial: () => {
      if (window.innerWidth > 786) {
        return { scale: 1 };
      } else {
        return { scale: 0.8 };
      }
    },
    hover: {
      scale: 0.8,
    },
  };

  return (
    <div className="flex flex-col items-center m-4">
      {typeof window !== "undefined" ? (
        <motion.figure
          variants={holder}
          whileHover="hover"
          initial="initial"
          className="flex justify-center items-center w-56 h-56 rounded-full border-2 hover:border-base-teal hover:border-4 border-black p-4 relative"
        >
          <motion.img
            variants={img}
            alt={member.name}
            className="rounded-full w-full h-full relative object-cover z-10 bg-white"
            src={member.img_url}
          />
          <Socials
            handles={[
              { github_id: member.github_id },
              { linkedin: member.linkedin },
              { twitter: member.twitter },
              { portfolio: member.portfolio },
            ]}
          />
        </motion.figure>
      ) : (
        <h3 className="flex items-center justify-center text-center text-lg lg:text-2xl font-medium text-base-black min-h-30">
          Loading...
        </h3>
      )}
      <h5 className="text-lg mt-6 font-medium">{member.name}</h5>
      <p className="text-sm">{`"${member.tagline}"`}</p>
    </div>
  );
};

export default Profile;
