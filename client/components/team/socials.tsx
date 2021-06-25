import { motion } from "framer-motion";

import { SocialIcon } from "../../utils/functions/socialIcon";

interface SocialsProps {
  handles: { [handle: string]: string }[];
}

const Socials = ({ handles }: SocialsProps) => {
  const jump = {
    intial: { scale: 1 },
    hover: (i) => {
      const Yval = (handles.length / 2 - i) * -40;
      const Xval = Math.abs(handles.length / 2 - i) * -10 + 90;
      return { x: Xval, y: Yval, scale: 1.1 };
    },
  };

  return (
    <>
      {handles.map((handle, key) => {
        return (
          <motion.div
            variants={jump}
            custom={key}
            className="w-4 h-4 absolute inset-1/2 z-0"
          >
            <SocialIcon handles={handle} />
          </motion.div>
        );
      })}
    </>
  );
};

export default Socials;
