import React, { useState, useEffect, useContext } from "react";
import { useRouter } from "next/router";
import OtherMaintainers from "../../../components/maintainer/dashboard/othermaintainers";
import { Layout } from "../../../components/shared";
import { successToast } from "../../../utils/functions/toast";
import { AuthContext } from "../../../context/authContext";
import { TiTick } from "react-icons/ti";
import {
  ContributorProps,
  OtherMaintainersProps,
} from "../../../utils/interfaces";
import Link from "next/link";
import CSSLoader from "../../../components/shared/loader";
import {
  postAcceptContributor,
  getContributorsApplications,
} from "../../../services/api";
import Footer from "../../../components/shared/footer";
import Loading from "../../../utils/icons/loading";

const headings = [
  "Name",
  "Email",
  "SRM",
  "Github",
  "Reg No",
  "Branch",
  "Proposal",
  "Maintainer Approval",
];

const ProjectDetail = () => {
  const [contributorsData, setContributorsData] = useState<ContributorProps[]>(
    []
  );
  const [maintainers, setMaintainers] = useState<OtherMaintainersProps[]>([]);
  const [projectName, setProjectName] = useState<string>("");
  const [projectId, setProjectId] = useState<string>("");
  const [accepted, setAccepted] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [loading2, setLoading2] = useState<boolean>(true);

  const router = useRouter();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (authContext.authReady) {
      if (!authContext.isAuth || authContext.isAdmin) {
        router.replace("/");
      }
    }
  }, [authContext]);

  const acceptContributorHandler = async (project_id, contributor_id) => {
    setLoading(true);
    const res = await postAcceptContributor(project_id, contributor_id);
    if (res) {
      setAccepted(true);
      successToast("Contributor Approved sucessfully!");
      setLoading(false);
    }
  };

  const _getContributorsApplications = async (token, slug) => {
    const res = await getContributorsApplications(token, slug);
    if (res) {
      setContributorsData(res.contributor);
      setProjectName(res.project_name);
      setProjectId(res._id);
      setMaintainers(res.maintainer);
      setLoading2(false);
    } else {
      setLoading2(false);
    }
  };

  useEffect(() => {
    const { slug } = router.query;
    const token = sessionStorage.getItem("token");
    _getContributorsApplications(token, slug);
  }, [router.query, accepted]);

  return !loading2 ? (
    <>
      <Layout type="maintainer">
        <div className="flex flex-col justify-center items-center">
          <h2 className="text-4xl font-extrabold text-white mb-5">
            {projectName}
          </h2>
          <OtherMaintainers
            otherMaintainers={maintainers?.filter(
              (m) => m.name !== authContext.username
            )}
          />
          <div className="overflow-auto w-full">
            {contributorsData?.length > 0 ? (
              <div className="text-white border-separate space-y-6 text-sm">
                <thead className="bg-base-teal text-white text-xl font-extrabold">
                  <tr>
                    {headings.map((head) => (
                      <th key={head} className="px-3 text-left">
                        {head}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {contributorsData?.map((person) => (
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

                      <td className="p-3 ">
                        {person.is_maintainer_approved ? (
                          <TiTick className="text-green-500 text-center text-3xl" />
                        ) : (
                          <button
                            onClick={() =>
                              acceptContributorHandler(projectId, person._id)
                            }
                            className="flex justify-center w-1/8 mx-auto mt-4 bg-green-400 p-2 font-bold text-white rounded-xl"
                          >
                            {loading ? <Loading /> : "Approve Contributor"}
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </div>
            ) : (
              <h2 className="text-4xl font-extrabold text-white mb-5 no-scrollbar">
                No contributor applications yet!!
              </h2>
            )}
          </div>
        </div>
      </Layout>
      <div className="fixed bottom-0 w-full">
        <Footer />
      </div>
    </>
  ) : (
    <div className="flex flex-col items-center justify-center w-screen min-h-screen bg-base-blue">
      <CSSLoader />
    </div>
  );
};

export default ProjectDetail;
