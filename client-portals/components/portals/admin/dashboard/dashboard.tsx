import Card from "../../../shared/card";
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

const AcceptedProjectDashboard = () => {
  return (
    <div className="min-h-screen p-14 bg-base-blue">
      <h2 className="text-4xl font-extrabold text-white mb-10">
        Hi, maintainer
      </h2>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 ">
        {PROJECTS.map((item) => (
          <Card name={item.name} id={item.id} desc={item.desc} key={item.id} />
        ))}
      </div>
    </div>
  );
};

export default AcceptedProjectDashboard;
