const ProjectCard = () => {
  const projectCardDetails = [
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src:
        "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["tailwind ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src:
        "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["python ", "django ", "vue"],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src:
        "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src:
        "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src:
        "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src:
        "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["python ", "django ", "vue"],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src:
        "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src:
        "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src:
        "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src:
        "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src:
        "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src:
        "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src:
        "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
  ];

  const COLORS = [
    "bg-base-black",
    "bg-base-green",
    "bg-base-smoke",
    "bg-base-blue",
    "bg-base-teal",
  ];

  return (
    <div>
      <h1 className="flex justify-center text-5xl font-bold mb-10 text-base-black">
        Projects
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {projectCardDetails.map((data) => (
          <div key={data.src} className="max-w-md  bg-gray-100">
            <div
              className={`${COLORS[Math.round(Math.random() * 4)]} px-20 py-1`}
            ></div>
            <div className="p-5">
              <div>
                <h2 className="text-gray-800 text-3xl font-semibold">
                  {data.name}
                </h2>
                <p className="mt-2 text-gray-600">{data.description}</p>
              </div>
              <div className="mt-2 mb-4">
                {data.tags.map((tag) => (
                  <p
                    className={`${
                      COLORS[Math.round(Math.random() * 4)]
                    } my-1 stracking-wider uppercase font-bold text-gray-100 mx-1 rounded p-2 inline-block cursor-default`}
                  >
                    {tag}
                  </p>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProjectCard;
