import { motion } from "framer-motion";
import { SocialIcon } from "../../utils/functions";

interface SocialsProps {
  handles: [
    { github_id?: string },
    { linkedin?: string },
    { twitter?: string },
    { portfolio?: string }
  ];
}

const Socials = ({ handles }: SocialsProps) => {
  const filteredHandles = handles.filter(
    (handle) => handle[Object.keys(handle)[0]].length !== 0
  );
  const len = filteredHandles.length;
  const hypo = 95;

  const angles = {
    1: [Math.PI / 4],
    2: [Math.PI / 4, Math.PI / 8],
    3: [Math.PI / 4, Math.PI / 8, 0],
    4: [Math.PI / 4, Math.PI / 8, 0, -Math.PI / 8],
  };
  const jump = {
    initial: (i) => {
      if (window.innerWidth >= 768) return {};

      const Yval = hypo * Math.sin(angles[len][i]);
      const Xval = hypo * Math.cos(angles[len][i]);
      return { x: Xval, y: Yval, scale: 1.1 };
    },
    hover: (i) => {
      if (window.innerWidth < 768) return {};

      const Yval = hypo * Math.sin(angles[len][i]);
      const Xval = hypo * Math.cos(angles[len][i]);
      return { x: Xval, y: Yval, scale: 1.1 };
    },
  };

  return (
    <>
      {typeof window !== "undefined" &&
        filteredHandles.map((handle, key) => (
          <motion.div
            key={key}
            variants={jump}
            custom={key}
            className="w-4 h-4 absolute z-0"
            transition={{ type: "string", default: { duration: 0.1 } }}
          >
            <SocialIcon handle={handle} />
          </motion.div>
        ))}
    </>
  );
};

export default Socials;
