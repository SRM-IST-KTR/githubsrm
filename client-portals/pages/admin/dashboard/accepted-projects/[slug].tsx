import React, { useState, useEffect, useContext } from "react";
import { useRouter } from "next/router";
import { AuthContext } from "../../../../context/authContext";
import { getProject, postAcceptProject } from "../../../../services/api";
import { successToast } from "../../../../utils/functions/toast";
import { Layout } from "../../../../components/shared";
import Link from "next/link";
import { ContributorsProps } from "../../../../utils/interfaces";
import CSSLoader from "../../../../components/shared/loader";
import Loading from "../../../../utils/icons/loading";
import Tick from "../../../../utils/icons/tick";
import Cross from "../../../../utils/icons/cross";

const headings = [
  "Name",
  "Email",
  "SRM",
  "Github",
  "Reg No",
  "Branch",
  "Proposal",
  "Maintainer approved?",
  "Added to repo?",
];

const ContributorsPage = () => {
  const [contributorsData, setContributorsData] = useState<ContributorsProps[]>(
    []
  );
  const [projectName, setProjectName] = useState<string>("");
  const [projectId, setProjectId] = useState<string>("");
  const [accepted, setAccepted] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [loading2, setLoading2] = useState<boolean>(true);

  const router = useRouter();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (authContext.authReady) {
      if (!authContext.isAuth || !authContext.isAdmin) {
        router.replace("/admin/dashboard/accepted-projects/", "/");
      }
    }
  }, [authContext]);

  const acceptMaintainerHandler = async (project_id, contributor_id) => {
    setLoading(true);
    const res = await postAcceptProject(project_id, contributor_id);
    if (res) {
      setAccepted(true);
      successToast("Contributor Approved sucessfully!");
      setLoading(false);
    }
  };

  const _getProject = async (slug, token) => {
    setLoading2(true);
    const res = await getProject(slug, token);
    if (res) {
      setContributorsData(res.contributor.contributor);
      setProjectName(res.project.project_name);
      setProjectId(res.project._id);
      setLoading2(false);
    }
  };

  useEffect(() => {
    const { slug } = router.query;
    const token = sessionStorage.getItem("token");
    _getProject(slug, token);
  }, [router.query, accepted]);

  return loading2 ? (
    <div className="flex flex-col items-center justify-center w-screen min-h-screen bg-base-blue">
      <CSSLoader />
    </div>
  ) : (
    <Layout type="admin">
      <h1 className="text-5xl font-extrabold underline text-white mb-7">
        {projectName}
      </h1>

      <div className="overflow-auto w-full">
        {contributorsData[0] ? (
          <table className="table text-white border-separate space-y-6 text-sm">
            <thead className="bg-base-teal text-white">
              <tr>
                {headings.map((head) => (
                  <th key={head} className="px-3 text-left">
                    {head}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {contributorsData.map((person) => (
                <tr key={person._id} className="bg-gray-800">
                  <td className="p-3">
                    <div className="flex align-items-center">
                      <div> {person.name}</div>
                    </div>
                  </td>
                  <td className="p-3">
                    <div className="flex align-items-center">
                      <div> {person.email}</div>
                    </div>
                  </td>
                  <td className="p-3">
                    <div className="flex align-items-center">
                      <div> {person.srm_email}</div>
                    </div>
                  </td>
                  <td className="p-3">
                    <div className="flex align-items-center">
                      <Link href={person.github_id}>
                        <div> {person.github_id}</div>
                      </Link>
                    </div>
                  </td>

                  <td className="p-3">
                    <div className="flex align-items-center">
                      <div> {person.reg_number}</div>
                    </div>
                  </td>
                  <td className="p-3">
                    <div className="flex align-items-center">
                      <div> {person.branch}</div>
                    </div>
                  </td>
                  <td className="p-3">
                    <div className="flex align-items-center">
                      <div> {person.poa}</div>
                    </div>
                  </td>
                  <td className="p-3">
                    <div className="flex align-items-center">
                      <div>
                        {" "}
                        {person.is_maintainer_approved ? (
                          <span className="text-green-500 text-2xl">
                            <Tick />
                          </span>
                        ) : (
                          <span className="text-red-500 text-lg">
                            <Cross />
                          </span>
                        )}
                      </div>
                    </div>
                  </td>
                  <td className="p-3">
                    <div className="flex align-items-center">
                      <div>
                        {" "}
                        {person.is_added_to_repo ? (
                          <span className="text-green-500 text-2xl">
                            <Tick />
                          </span>
                        ) : (
                          <span className="text-red-500 text-lg">
                            <Cross />
                          </span>
                        )}
                      </div>
                    </div>
                  </td>
                  <td className="p-3 ">
                    {person.is_admin_approved ? (
                      <span className="text-green-500 text-center text-3xl">
                        <Tick />
                      </span>
                    ) : (
                      <button
                        onClick={() =>
                          acceptMaintainerHandler(projectId, person._id)
                        }
                        className="flex justify-center w-1/8 mx-auto mt-4 bg-green-400 p-2 font-bold text-white rounded-xl"
                      >
                        {loading ? (
                          <span className="flex w-6 mx-auto">
                            <Loading />
                          </span>
                        ) : (
                          "Approve Contributor"
                        )}
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <h1 className="text-5xl text-gray-200 mt-10 overflow-auto no-scrollbar">
            No Contributors Yet!!
          </h1>
        )}
      </div>
    </Layout>
  );
};

export default ContributorsPage;
