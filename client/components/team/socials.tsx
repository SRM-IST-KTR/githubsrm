import { motion, useElementScroll, useTransform } from "framer-motion";

import { GitHubIcon } from "../../utils/icons";

interface SocialsProps {
  handles: { [handle: string]: string }[];
}

const Socials = ({ handles }: SocialsProps) => {
  return (
    <motion.div className="relative">
      <div className="w-4 h-4 absolute ">
        <GitHubIcon />
      </div>
    </motion.div>
  );
};

export default Socials;
