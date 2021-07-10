import Adminnavbar from "./navbar";
import Card from "../../../shared/card";

const PROJECTS = [
  {
    name: "Project 1",
    id: "1",
    desc:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Tempora expedita dicta totam aspernatur doloremque. Excepturi iste iusto eos",
  },
  {
    name: "Project 2",
    id: "2",
    desc:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Tempora expedita dicta totam aspernatur doloremque. Excepturi iste iusto eos",
  },
  {
    name: "Project 3",
    id: "3",
    desc:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Tempora expedita dicta totam aspernatur doloremque. Excepturi iste iusto eos",
  },
  {
    name: "Project 4",
    id: "4",
    desc:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Tempora expedita dicta totam aspernatur doloremque. Excepturi iste iusto eos",
  },
  {
    name: "Project 5",
    id: "5",
    desc:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Tempora expedita dicta totam aspernatur doloremque. Excepturi iste iusto eos",
  },
];

const AcceptedProjectsCard = () => {
  return (
    <div className="p-10">
      <Adminnavbar />
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 ">
        {PROJECTS.map((item) => (
          <Card
            url={`/admin/dashboard/accepted-projects/${item.id}`}
            name={item.name}
            desc={item.desc}
            key={item.id}
          />
        ))}
      </div>
    </div>
  );
};

export default AcceptedProjectsCard;
