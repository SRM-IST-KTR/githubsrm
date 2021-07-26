import React, { useState, useEffect, useContext } from "react";
import { useRouter } from "next/router";
import OtherMaintainers from "components/maintainer/dashboard/other-maintainers";
import { Layout, Button } from "@/shared/index";
import { successToast, alertToast } from "utils/functions/toast";
import { AuthContext } from "context/authContext";
import { ContributorProps, OtherMaintainersProps } from "utils/interfaces";
import CSSLoader from "components/shared/loader";
import {
  postAcceptContributor,
  getContributorsApplications,
  deletefromMaintainerContributor,
} from "services/api";
import { Loading, Tick, Cross } from "@/icons/index";
import { PaginationButtons } from "@/shared/index";

const headings = [
  "Name",
  "Email",
  "SRM Email",
  "Github",
  "Reg No",
  "Branch",
  "Proposal",
  "Maintainer Approval",
  "Maintainer Rejection",
];

const ProjectDetail = () => {
  const [contributorsData, setContributorsData] = useState<ContributorProps[]>(
    []
  );
  const [maintainers, setMaintainers] = useState<OtherMaintainersProps[]>([]);
  const [projectName, setProjectName] = useState<string>("");
  const [projectId, setProjectId] = useState<string>("");
  const [clickedAcceptBtn, setClickedAcceptBtn] = useState<string>("");
  const [clickedRejectBtn, setClickedRejectBtn] = useState<string>("");
  const [hasNextPage, sethasNextPage] = useState<boolean>(false);
  const [hasPrevPage, sethasPrevPage] = useState<boolean>(false);
  const [accepted, setAccepted] = useState<boolean>(false);
  const [rejected, setRejected] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [loading2, setLoading2] = useState<boolean>(true);
  const [rejectLoading, setRejectLoading] = useState<boolean>(false);
  const [cPageNo, setCPageNo] = useState<number>(1);

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
    setClickedAcceptBtn(contributor_id);
    setLoading(true);
    const res = await postAcceptContributor(project_id, contributor_id);
    if (res) {
      setAccepted(true);
      successToast("Contributor Approved sucessfully!");
      setLoading(false);
    }
  };

  const deleteContributorHandler = async (contributor_id) => {
    setClickedRejectBtn(contributor_id);
    setRejectLoading(true);
    const res = await deletefromMaintainerContributor(contributor_id);
    if (res) {
      setRejected(true);
      alertToast("Contributor Rejected successfully!");
      setRejectLoading(false);
    } else {
      setRejectLoading(false);
    }
  };

  const _getContributorsApplications = async (slug) => {
    const res = await getContributorsApplications(slug, cPageNo, 1);
    if (res) {
      setContributorsData(res.contributor);
      setProjectName(res.project_name);
      setProjectId(res._id);
      setMaintainers(res.maintainer);
      sethasNextPage(res.contributorHasNextPage);
      if (cPageNo > 1) {
        sethasPrevPage(true);
      }
      setLoading2(false);
    } else {
      setLoading2(false);
    }
  };

  useEffect(() => {
    const { slug } = router.query;
    if (slug) {
      _getContributorsApplications(slug);
    }
  }, [router.query, accepted, rejected, cPageNo]);

  return !loading2 ? (
    <Layout type="maintainer">
      <div className="flex flex-col justify-center items-center">
        <h2 className="text-5xl font-extrabold text-gray-50 my-1">
          {projectName}
        </h2>
        <OtherMaintainers
          otherMaintainers={maintainers?.filter(
            (m) => m.name !== authContext.username
          )}
        />
        <div className="overflow-auto w-full">
          {contributorsData?.length > 0 && (
            <h2 className="mr-5 mb-5 font-bold text-white text-3xl text-center">
              Contributors' Applications
            </h2>
          )}
          {contributorsData?.length > 0 ? (
            <>
              <div className="text-white border-separate md:space-y-6 space-y-2 text-sm overflow-auto">
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
                          <a
                            className="hover:text-base-teal"
                            target="_blank"
                            rel="noopener noreferrer"
                            href={`https://github.com/${person.github_id}`}
                          >
                            <div> {person.github_id}</div>
                          </a>
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
                        {person.is_maintainer_approved &&
                        !person.is_maintainer_rejected ? (
                          <span className="text-green-500 text-center text-3xl">
                            <Tick />
                          </span>
                        ) : person.is_maintainer_rejected ? (
                          <span className="text-red-500 text-center text-xl">
                            <Cross />
                          </span>
                        ) : (
                          <Button
                            onClick={() =>
                              acceptContributorHandler(projectId, person._id)
                            }
                          >
                            {loading && clickedAcceptBtn === person._id ? (
                              <span className="flex w-6 mx-auto">
                                <Loading />
                              </span>
                            ) : (
                              "Approve Contributor"
                            )}
                          </Button>
                        )}
                      </td>
                      <td className="p-3 ">
                        {person.is_maintainer_rejected &&
                        !person.is_maintainer_approved ? (
                          <span className="text-green-500 text-center text-3xl">
                            <Tick />
                          </span>
                        ) : person.is_maintainer_approved ? (
                          <span className="text-red-500 text-center text-xl">
                            <Cross />
                          </span>
                        ) : (
                          <button
                            className="flex justify-center w-1/8 mx-auto mt-4 bg-red-400 p-2 font-bold text-white rounded-xl"
                            onClick={() => deleteContributorHandler(person._id)}
                          >
                            {rejectLoading &&
                            clickedRejectBtn === person._id ? (
                              <span className="flex w-6 mx-auto">
                                <Loading />
                              </span>
                            ) : (
                              "Reject Contributor"
                            )}
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </div>
              <div className="mt-4">
                <PaginationButtons
                  hasNextPage={hasNextPage}
                  hasPrevPage={hasPrevPage}
                  pageNo={cPageNo}
                  setPageNo={setCPageNo}
                />
              </div>
            </>
          ) : (
            <h2 className="text-4xl text-center mt-10  text-white mb-5 no-scrollbar">
              No contributor applications yet!!
            </h2>
          )}
        </div>
      </div>
    </Layout>
  ) : (
    <Layout type="maintainer">
      <div className="flex flex-col items-center justify-center">
        <CSSLoader />
      </div>
    </Layout>
  );
};

export default ProjectDetail;
