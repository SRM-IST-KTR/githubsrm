import React, { useState } from "react";
import { TiTick } from "react-icons/ti";
import { ImCross } from "react-icons/im";
import { FaGithub } from "react-icons/fa";
import { successToast } from "../../utils/functions/toast";
import { tableData } from "./tableData";

const ProjectTable = () => {
  const [selectedContributor, setSelectedContributor] = useState("");

  const tableHeading = [
    "Name",
    "Email",
    "GitHub ID",
    "SRM Email",
    "Registration Number",
    "Branch",
    "Maintainer Approval",
  ];

  const submitHandler = (id) => {
    setSelectedContributor(id);
    // post selectedContributor here
    console.log(selectedContributor);
    successToast("Contributor Approved sucessfully!");
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
                        {data.github_id}
                      </a>
                    </td>
                    <td className="p-3">
                      <a href="mailto:{data.srm_email}">{data.srm_email}</a>
                    </td>
                    <td className="p-3">{data.reg_number}</td>
                    <td className="p-3">{data.branch}</td>
                    <td className="p-3 ">
                      {data.maintainer_approved === "true" ? (
                        <TiTick className="text-green-500 text-2xl" />
                      ) : (
                        <button
                          onClick={() => submitHandler(data.id)}
                          className="flex justify-center w-1/8 mx-auto mt-4 bg-green-400 p-2 font-bold text-white rounded-xl"
                        >
                          Approve
                        </button>
                      )}
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
