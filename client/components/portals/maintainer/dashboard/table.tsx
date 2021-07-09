const ProjectTable = () => {
  const tableData = [
    {
      name: "Contributor 1",
      email: "test@test.com",
      github_id: "sample",
      srm_email: "test@srmist.edu.in",
      reg_number: "RA19110300100xx",
      branch: "CSE",
      projectID: "1",
      maintainer_approved: "true",
    },
    {
      name: "Contributor 2",
      email: "test@test.com",
      github_id: "sample",
      srm_email: "test@srmist.edu.in",
      reg_number: "RA19110300100xx",
      branch: "CSE",
      projectID: "2",
      maintainer_approved: "true",
    },
    {
      name: "Contributor 3",
      email: "test@test.com",
      github_id: "sample",
      srm_email: "test@srmist.edu.in",
      reg_number: "RA1911030010026",
      branch: "CSE",
      projectID: "3",
      maintainer_approved: "true",
    },
  ];
  return (
    <>
      <div className="flex justify-center">
        <div className="col-span-12">
          <div className="overflow-auto lg:overflow-visible ">
            <table className="table text-white border-separate space-y-6 text-sm">
              <thead className="bg-gray-800 text-white">
                <tr>
                  <th className="p-3 text-left">Name</th>
                  <th className="p-3 text-left">Email</th>
                  <th className="p-3 text-left">Github id</th>
                  <th className="p-3 text-left">SRM Email</th>
                  <th className="p-3 text-left">Registration Number</th>
                  <th className="p-3 text-left">Branch</th>
                  {/* // TODO: remove project id */}
                  <th className="p-3 text-left">Project ID</th>
                  <th className="p-3 text-left">Maintainer Approval</th>
                </tr>
              </thead>
              <tbody>
                {tableData.map((data) => (
                  <tr className="bg-gray-800">
                    <td className="p-3">
                      <div className="flex align-items-center">
                        <div className="">{data.name}</div>
                      </div>
                    </td>
                    <td className="p-3">{data.email}</td>
                    <td className="p-3">{data.github_id}</td>
                    <td className="p-3">{data.srm_email}</td>
                    <td className="p-3">{data.reg_number}</td>
                    <td className="p-3">{data.branch}</td>
                    <td className="p-3">{data.projectID}</td>
                    <td className="p-3 ">
                      <a
                        href="#"
                        className="text-white hover:text-gray-100 mr-2"
                      >
                        {/* // TODO: Add toggle for on/off */}
                        <button className="bg-green-400 p-2 text-white rounded-xl">
                          {data.maintainer_approved}
                        </button>
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </>
  );
};

export default ProjectTable;
