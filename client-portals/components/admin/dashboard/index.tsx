import React, { useEffect, useState } from "react";
import instance from "../../../services/api";
import { TiTick } from "react-icons/ti";
import { GrNext, GrPrevious } from "react-icons/gr";
import { successToast, errToast } from "../../../utils/functions/toast";
import Link from "next/link";
import { Layout } from "../../shared";
import { getRecaptchaToken } from "../../../services/recaptcha";
import { TableProjectsProps } from "../../../utils/interfaces";

const ProjectApplications = () => {
  const [tableDataProjects, setTableDataProjects] = useState<
    TableProjectsProps[]
  >([]);
  const [accepted, setAccepted] = useState<boolean>(false);
  const [pageNo, setPageNo] = useState<number>(1);
  const [hasNextPage, sethasNextPage] = useState<boolean>(false);
  const [hasPrevPage, sethasPrevPage] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  const headings = [
    "Maintainers",
    "Project Name",
    "Project Url",
    "Tags",
    "Private",
    "Project Description",
  ];

  const acceptProjectHandler = async (project_id, isprivate, project_url) => {
    const recaptchaToken = await getRecaptchaToken("post");
    const token = sessionStorage.getItem("token");
    await instance
      .post(
        `admin/projects?projectId=${project_id}&role=project`,
        {
          project_id: project_id,
          private: isprivate,
          project_url: project_url,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "X-RECAPTCHA-TOKEN": recaptchaToken,
          },
        }
      )
      .then((res) => {
        setAccepted(true);
        successToast("Project Approved sucessfully!");
      })
      .catch((err) => {
        errToast(err.message);
      });
  };

  useEffect(() => {
    const token = sessionStorage.getItem("token");
    instance
      .get(`admin/projects?page=${pageNo}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((res) => {
        setTableDataProjects(res.data.records);
        sethasNextPage(res.data.hasNextPage);
        sethasPrevPage(res.data.hasPreviousPage);
        setLoading(false);
      })
      .catch((err) => {
        setLoading(false);
      });
  }, [accepted, pageNo]);

  return !loading ? (
    <Layout type="admin">
      <div className="overflow-scroll">
        <h2 className="text-gray-50 m-2 font-medium">Page- {pageNo}</h2>
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
            {tableDataProjects.map((data) => (
              <tr key={data._id} className="bg-gray-800">
                <td className="p-3">
                  <div className="flex align-items-center">
                    <Link href={`/admin/dashboard/${data._id}`}>
                      <div className="cursor-pointer rounded-lg bg-gray-700 p-3 hover:bg-gray-900">
                        Open
                      </div>
                    </Link>
                  </div>
                </td>
                <td className="p-3">
                  <div className="flex align-items-center">
                    <div>{data.project_name}</div>
                  </div>
                </td>
                <td className="p-3">
                  <div className="flex align-items-center">
                    <div>{data.project_url}</div>
                  </div>
                </td>
                <td className="p-3">
                  <div className="flex align-items-center">
                    <div>
                      {data.tags.map((tag) => (
                        <p key={tag}>{tag}</p>
                      ))}
                    </div>
                  </div>
                </td>
                <td className="p-3">
                  <div className="flex align-items-center">
                    <div>{data.private ? "private" : "public"}</div>
                  </div>
                </td>
                <td className="p-3 w-44">
                  <div className="flex align-items-center  overflow-scroll">
                    <div>{data.description}</div>
                  </div>
                </td>
                <td className="p-3 ">
                  {data.is_admin_approved ? (
                    <TiTick className="text-green-500 text-4xl" />
                  ) : (
                    <button
                      onClick={() =>
                        acceptProjectHandler(
                          data._id,
                          data.private,
                          data.project_url
                        )
                      }
                      className="flex justify-center w-1/8 mx-auto mt-4 bg-green-400 p-2 font-bold text-white rounded-xl"
                    >
                      Approve project
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex justify-center my-5">
        <button
          disabled={!hasPrevPage}
          className={`${
            !hasPrevPage
              ? "opacity-10 cursor-not-allowed"
              : "hover:bg-base-green focus:bg-base-green"
          } p-3 rounded-full`}
          onClick={() => setPageNo(pageNo - 1)}
        >
          <GrPrevious className="text-2xl font-extrabold" />
        </button>
        <h2 className="text-gray-50 text-4xl  font-medium mx-3">{pageNo}</h2>
        <button
          disabled={!hasNextPage}
          className={`${
            !hasNextPage
              ? "opacity-10 cursor-not-allowed"
              : "hover:bg-base-green focus:bg-base-green"
          } p-3 rounded-full`}
          onClick={() => setPageNo(pageNo + 1)}
        >
          <GrNext className="text-2xl font-extrabold" />
        </button>
      </div>
    </Layout>
  ) : (
    <div className="min-h-screen flex justify-center p-5 bg-base-blue">
      <h1 className="text-7xl font-extrabold text-gray-100 text-center pt-20 animate-pulse">
        loading..
      </h1>
    </div>
  );
};

export default ProjectApplications;
