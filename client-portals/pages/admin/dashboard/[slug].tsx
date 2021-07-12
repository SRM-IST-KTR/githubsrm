import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import AuthContextProvider from "../../../context/authContext";
import instance from "../../../services/api";
import { successToast, errToast } from "../../../utils/functions/toast";
import { TiTick } from "react-icons/ti";

const MaintainerPage = () => {
  const [maintainerData, setMaintainerData] = useState([]);
  const [projectName, setProjectName] = useState("");
  const [projectId, setProjectId] = useState("");
  const [accepted, setAccepted] = useState<boolean>(false);

  const router = useRouter();

  const token = sessionStorage.getItem("token");

  const acceptMaintainerHandler = (project_id, maintainer_id) => {
    instance
      .post(
        "admin/projects?role=maintainer",
        { project_id: project_id, maintainer_id: maintainer_id },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "X-RECAPTCHA-TOKEN": null,
          },
        }
      )
      .then((res) => {
        console.log(res);
        setAccepted(true);
        successToast("Maintainer Approved sucessfully!");
      })
      .catch((err) => {
        errToast(err.message);
      });
  };

  useEffect(() => {
    const { slug } = router.query;
    instance
      .get(
        `admin/projects?projectId=${slug}&contributor=false&maintainer=true`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "X-RECAPTCHA-TOKEN": null,
          },
        }
      )
      .then((res) => {
        setMaintainerData(res.data.maintainer.maintainer);
        setProjectName(res.data.project.project_name);
        setProjectId(res.data.project._id);
      })
      .catch((err) => {
        errToast(err.message);
      });
  }, [accepted]);

  useEffect(() => {
    if (!sessionStorage.getItem("token")) {
      router.push("/admin");
    }
  }, []);

  return (
    <AuthContextProvider>
      <div className="flex flex-col items-center min-h-screen p-14 bg-base-blue">
        <h1 className="text-6xl font-extrabold underline text-white mb-5">
          MAINTAINERS
        </h1>
        <h1 className="text-5xl font-bold  text-white mb-7">
          Project: {projectName}
        </h1>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 ">
          {maintainerData.map((person) => (
            <div
              key={person._id}
              className="p-5 rounded-xl border-4 border-gray-100 shadow-xl"
            >
              <h2 className="text-2xl font-medium text-white mb-5">
                {person.name}
              </h2>
              <h2 className="text-2xl font-medium text-white mb-5">
                {person.email}
              </h2>
              <h2 className="text-2xl font-medium text-white mb-5">
                {person.github_id}
              </h2>
              <h2 className="text-2xl font-medium text-white mb-5">
                {person.reg_number}
              </h2>
              <h2 className="text-2xl font-medium text-white mb-5">
                {person.branch}
              </h2>
              {person.is_admin_approved ? (
                <div className="flex flex-col justify-center items-center text-4xl font-medium text-base-green mt-5">
                  <TiTick className="text-green-500 text-5xl" />
                  <p> approved</p>
                </div>
              ) : (
                <button
                  onClick={() => acceptMaintainerHandler(projectId, person._id)}
                  className="flex justify-center w-1/8 mx-auto mt-4 bg-green-400 p-2 font-bold text-white rounded-xl"
                >
                  Approve Maintainer
                </button>
              )}
            </div>
          ))}
        </div>
      </div>
    </AuthContextProvider>
  );
};

export default MaintainerPage;
