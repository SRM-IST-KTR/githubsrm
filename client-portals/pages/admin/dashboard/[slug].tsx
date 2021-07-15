import React, { useState, useEffect, useContext } from "react";
import { useRouter } from "next/router";
import { AuthContext } from "../../../context/AuthContext";
import instance from "../../../services/api";
import { successToast, errToast } from "../../../utils/functions/toast";
import { TiTick } from "react-icons/ti";
import { FiGithub } from "react-icons/fi";
import { Layout } from "../../../components/shared";
import Link from "next/link";
import { getRecaptchaToken } from "../../../services/recaptcha";
import { MaintainersProps } from "../../../utils/interfaces";

const MaintainerPage = () => {
  const [maintainerData, setMaintainerData] = useState<MaintainersProps[]>([]);
  const [projectName, setProjectName] = useState<string>("");
  const [projectId, setProjectId] = useState<string>("");
  const [accepted, setAccepted] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  const router = useRouter();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (authContext.isAuth === false) {
      router.push("/admin");
    }
  }, [authContext]);

  var token = null;
  useEffect(() => {
    token = sessionStorage.getItem("token");
  }, []);

  const acceptMaintainerHandler = async (project_id, maintainer_id) => {
    const recaptchaToken = await getRecaptchaToken("post");
    await instance
      .post(
        "admin/projects?role=maintainer",
        { project_id: project_id, maintainer_id: maintainer_id },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "X-RECAPTCHA-TOKEN": recaptchaToken,
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
          },
        }
      )
      .then((res) => {
        setMaintainerData(res.data.maintainer.maintainer);
        setProjectName(res.data.project.project_name);
        setProjectId(res.data.project._id);
        setLoading(false);
      })
      .catch((err) => {
        errToast(err.message);
        setLoading(false);
      });
  }, [accepted]);

  return loading ? (
    <div className="min-h-screen flex justify-center p-5 bg-base-blue">
      <h1 className="text-7xl font-extrabold text-gray-100 text-center pt-20 animate-pulse">
        loading..
      </h1>
    </div>
  ) : (
    <Layout type="admin">
      <h1 className="text-4xl text-center font-extrabold text-white mb-7">
        All maintainer applications of {projectName}
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 ">
        {maintainerData.map((person) => (
          <div key={person._id} className="p-5 rounded-xl  shadow-2xl">
            <h2 className="text-2xl font-medium text-white mb-5">
              {person.name}
            </h2>
            <h2 className="text-2xl font-medium text-white mb-5">
              {person.email}
            </h2>
            <Link href={person.github_id}>
              <div className="cursor-pointer hover:text-gray-800 p-2  flex text-2xl font-medium text-white mb-5">
                <FiGithub /> <span className="ml-1">{person.github_id}</span>
              </div>
            </Link>
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
    </Layout>
  );
};

export default MaintainerPage;
