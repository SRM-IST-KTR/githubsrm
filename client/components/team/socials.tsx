import { motion } from "framer-motion";
import { fileURLToPath } from "url";

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
  const filteredHandels = handles.filter(
    (handle) => handle[Object.keys(handle)[0]].length !== 0
  );
  const len = filteredHandels.length;
  const hypo = 95;
  const closeness = 1;
  const angles = {
    1: [0],
    2: [(Math.PI / 8) * closeness, (-Math.PI / 8) * closeness],
    3: [(Math.PI / 4) * closeness, 0, (-Math.PI / 4) * closeness],
    4: [
      (Math.PI / 4) * closeness,
      (Math.PI / 8) * closeness,
      0 * closeness,
      (-Math.PI / 8) * closeness,
    ],
  };
  const jump = {
    hover: (i) => {
      const Yval = hypo * Math.sin(angles[len][i]);
      const Xval = hypo * Math.cos(angles[len][i]);
      return { x: Xval, y: Yval, scale: 1.1 };
    },
  };

  return (
    <>
      {filteredHandels.map((handle, key) => (
        <motion.div
          key={key}
          variants={jump}
          custom={key}
          className="w-4 h-4 absolute z-0"
          transition={{ type: "string ", default: { duration: 0.1 } }}
        >
          <SocialIcon handle={handle} />
        </motion.div>
      ))}
    </>
  );
};

export default Socials;
