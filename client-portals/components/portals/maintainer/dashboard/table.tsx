import React, { useState } from "react";

const ProjectTable = () => {
  const [selectedContributors, setSelectedContributors] = useState([]);
  const tableHeading = [
    "Name",
    "Id",
    "Email",
    "GitHub ID",
    "SRM Email",
    "Registration Number",
    "Branch",
    "Maintainer Approval",
  ];
  const tableData = [
    {
      id: "1",
      name: "Contributor 1",
      email: "test@test.com",
      github_id: "sample",
      srm_email: "test@srmist.edu.in",
      reg_number: "RA19110300100xx",
      branch: "CSE",
      maintainer_approved: "true",
    },
    {
      id: "2",
      name: "Contributor 2",
      email: "test@test.com",
      github_id: "sample",
      srm_email: "test@srmist.edu.in",
      reg_number: "RA19110300100xx",
      branch: "CSE",
      maintainer_approved: "true",
    },
    {
      id: "3",
      name: "Contributor 3",
      email: "test@test.com",
      github_id: "sample",
      srm_email: "test@srmist.edu.in",
      reg_number: "RA1911030010026",
      branch: "CSE",
      maintainer_approved: "true",
    },
  ];

  const submitHandler = () => {
    console.log(selectedContributors);
  };

  return (
    <>
      <div className="flex justify-center">
        <div className="col-span-12">
          <div className="overflow-auto lg:overflow-visible ">
            <table className="table text-white border-separate space-y-6 text-sm">
              <thead className="bg-gray-800 text-white">
                <tr>
                  {tableHeading.map((heading) => (
                    <th key={heading} className="px-3 text-left">
                      {heading}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {tableData.map((data) => (
                  <tr key={data.id} className="bg-gray-800">
                    <td className="p-3">
                      <div className="flex align-items-center">
                        <div className="">{data.name}</div>
                      </div>
                    </td>
                    <td className="p-3">{data.id}</td>
                    <td className="p-3">{data.email}</td>
                    <td className="p-3">{data.github_id}</td>
                    <td className="p-3">{data.srm_email}</td>
                    <td className="p-3">{data.reg_number}</td>
                    <td className="p-3">{data.branch}</td>
                    <td className="p-3 ">
                      <a
                        href="#"
                        className="text-white hover:text-gray-100 mr-2"
                      >
                        {/* // TODO: Add checkbox */}
                        <input
                          type="checkbox"
                          className="apprearance-none text-center checked:bg-blue-600 checked:border-transparent"
                          value={data.id}
                          onChange={(e) =>
                            setSelectedContributors([
                              ...selectedContributors,
                              e.target.value,
                            ])
                          }
                        ></input>
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <button
        onClick={submitHandler}
        className="flex justify-center w-1/8 mx-auto mt-4 bg-green-400 p-2 text-white rounded-xl"
      >
        Submit
      </button>
    </>
  );
};

export default ProjectTable;
