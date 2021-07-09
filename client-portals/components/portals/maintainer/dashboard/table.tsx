import React, { useState } from "react";
import { TiTick } from "react-icons/ti";
import { ImCross } from "react-icons/im";
import { FaGithub } from "react-icons/fa";
import { successToast } from "../../../../utils/functions/toast";

const ProjectTable = () => {
  const [selectedContributors, setSelectedContributors] = useState([]);
  const [approve, setApprove] = useState(false);
  const tableHeading = [
    "Name",
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
    setApprove(true);
    successToast("Contributors Approved sucessfully!");
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

                    <td className="p-3">
                      <a href="mailto:{data.email}">{data.email}</a>
                    </td>
                    <td className="p-3">
                      <a href={data.github_id}>
                        <FaGithub className="text-2xl" />
                      </a>
                    </td>
                    <td className="p-3">
                      <a href="mailto:{data.srm_email}">{data.srm_email}</a>
                    </td>
                    <td className="p-3">{data.reg_number}</td>
                    <td className="p-3">{data.branch}</td>
                    <td className="p-3 ">
                      {!approve ? (
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
                      ) : selectedContributors.find((c) => c === data.id) ? (
                        <TiTick className="text-green-500 text-2xl" />
                      ) : (
                        <ImCross className="text-red-500" />
                      )}
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
        className="flex justify-center w-1/8 mx-auto mt-4 bg-green-400 p-4 font-bold text-white rounded-xl"
      >
        Approve
      </button>
    </>
  );
};

export default ProjectTable;
