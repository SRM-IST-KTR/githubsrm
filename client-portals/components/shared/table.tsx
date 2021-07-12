import React, { useState, useEffect } from "react";
import { TiTick } from "react-icons/ti";
import { ImCross } from "react-icons/im";
import { FaGithub } from "react-icons/fa";
import { successToast } from "../../utils/functions/toast";

const ProjectTable = ({ tableData }) => {
  const [selectedContributor, setSelectedContributor] = useState("");

  const submitHandler = (id) => {
    setSelectedContributor(id);
    // post selectedContributor here
    console.log(selectedContributor);
    successToast("Contributor Approved sucessfully!");
  };

  var headings = Object.keys(tableData[2]);
  var row_values = [];

  useEffect(() => {
    for (var i = 0; i < tableData.length; i++) {
      row_values.push(Object.values(tableData[i]));
    }
    console.log(row_values);
  }, []);

  return (
    <>
      <div className="flex justify-center">
        <div className="col-span-12">
          <div className="overflow-auto lg:overflow-visible ">
            <table className="table text-white border-separate space-y-6 text-sm">
              <thead className="bg-gray-800 text-white">
                <tr>
                  {headings.map((head) => (
                    <th className="px-3 text-left">{head}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {tableData.map((data) => (
                  <tr key={data} className="bg-gray-800">
                    <td className="p-3">
                      <div className="flex align-items-center">
                        <div>{data}</div>
                      </div>
                    </td>

                    {/* <td className="p-3 ">
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
                    </td> */}
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
