import { motion } from "framer-motion";

import { SocialIcon } from "../../utils/functions/social-icon";

interface SocialsProps {
  handles: [
    { github_id: string },
    { linkedin: string },
    { twitter: string },
    { portfolio: string }
  ];
}

const Socials = ({ handles }: SocialsProps) => {
  const jump = {
    hover: (i) => {
      const Yval = (handles.length / 2 - i) * -30;
      const Xval = Math.abs(handles.length / 2 - i) * -10 + 90;
      return { x: Xval, y: Yval, scale: 1.1 };
    },
  };

  return (
    <>
      {handles.map((handle, key) => (
        <motion.div
          key={key}
          variants={jump}
          custom={key}
          className="w-4 h-4 absolute inset-1/2 z-0"
          transition={{ type: "string ", default: { duration: 0.1 } }}
        >
          <SocialIcon handle={handle} />
        </motion.div>
      ))}
    </>
  );
};

export default Socials;
