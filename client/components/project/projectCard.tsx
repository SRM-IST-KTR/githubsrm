const ProjectCard = () => {
  const projectCardDetails = [
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
    {
      name: "Project Name",
      description:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
      src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      tags: ["web-app ", "javascript ", "typescript "],
    },
  ];
  return (
    <div>
      <h1 className="flex justify-center text-5xl font-bold mb-10 text-base-black">
        Projects
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {projectCardDetails.map((data) => (
          <div
            key={data.src}
            className="max-w-md py-4 px-8 bg-white shadow-lg rounded-lg"
          >
            <div className="flex justify-center md:justify-end -mt-16">
              <img
                className="w-20 h-20 object-cover rounded-full border-2 border-base-black-500"
                src={data.src}
              />
            </div>
            <div>
              <h2 className="text-gray-800 text-3xl font-semibold">
                {data.name}
              </h2>
              <p className="mt-2 text-gray-600">{data.description}</p>
            </div>
            <div className="mx-1 mt-2 mb-4">
              {data.tags.map((tag) => (
                <p className="my-1 stracking-wider uppercase font-bold text-gray-700 mx-1 bg-gray-100 rounded p-2 inline-block cursor-default">
                  {tag}
                </p>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProjectCard;
