import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import ProjectTable from "../../../components/shared/table";
import OtherMaintainers from "../../../components/portals/maintainer/dashboard/othermaintainers";

const PROJECTS = [
  {
    name: "Project 1",
    id: "1",
    desc: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Tempora expedita dicta totam aspernatur doloremque. Excepturi iste iusto eos",
  },
  {
    name: "Project 2",
    id: "2",
    desc: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Tempora expedita dicta totam aspernatur doloremque. Excepturi iste iusto eos",
  },
  {
    name: "Project 3",
    id: "3",
    desc: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Tempora expedita dicta totam aspernatur doloremque. Excepturi iste iusto eos",
  },
  {
    name: "Project 4",
    id: "4",
    desc: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Tempora expedita dicta totam aspernatur doloremque. Excepturi iste iusto eos",
  },
  {
    name: "Project 5",
    id: "5",
    desc: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Tempora expedita dicta totam aspernatur doloremque. Excepturi iste iusto eos",
  },
];

const ProjectDetail = () => {
  const [project, setProject] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const { slug } = router.query;
    const found = PROJECTS.find((p) => p.id === slug);
    setProject(found);
  }, [project]);

  if (project === null) {
    return <p>loading...... </p>;
  }

  return project ? (
    <div className="min-h-screen p-14 bg-base-blue">
      <h2 className="text-4xl font-extrabold text-white mb-5">
        {project.name}
      </h2>
      <h2 className="text-2xl font-medium text-white mb-10">{project.desc}</h2>
      <OtherMaintainers />
      <ProjectTable />
    </div>
  ) : (
    <div>
      <p>not found </p>
    </div>
  );
};

export default ProjectDetail;
