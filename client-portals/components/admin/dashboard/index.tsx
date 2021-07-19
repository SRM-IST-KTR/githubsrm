import React, { useEffect, useState } from "react";
import instance from "../../../services/api";
import { TiTick } from "react-icons/ti";
import { GrNext, GrPrevious } from "react-icons/gr";
import Link from "next/link";
import { Layout } from "../../shared";
import { TableProjectsProps } from "../../../utils/interfaces";
import CSSLoader from "../../shared/loader";
import ProjectVisibility from "./project-visibility-popup";
import { errorHandler } from "../../../services/api";
import Footer from "../../shared/footer";

const ProjectApplications = () => {
  const [tableDataProjects, setTableDataProjects] = useState<
    TableProjectsProps[]
  >([]);
  const [pageNo, setPageNo] = useState<number>(1);
  const [hasNextPage, sethasNextPage] = useState<boolean>(false);
  const [hasPrevPage, sethasPrevPage] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [open, setOpen] = useState<boolean>(false);
  const [projId, setProjId] = useState<string>("");

  const headings = [
    "Maintainers",
    "Project Name",
    "Project Url",
    "Tags",
    "Private",
    "Project Description",
    "Project Approval",
  ];

  useEffect(() => {
    let mounted = true;
    const token = sessionStorage.getItem("token");
    instance
      .get(`admin/projects?page=${pageNo}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((res) => {
        if (mounted) {
          setTableDataProjects(res.data.records);
          sethasNextPage(res.data.hasNextPage);
          sethasPrevPage(res.data.hasPreviousPage);
        }
        setLoading(false);
      })
      .catch((err) => {
        setLoading(false);
      });

    return () => {
      mounted = false;
    };
  }, [pageNo]);

  return !loading ? (
    <>
      <Layout type="admin">
        <div className="overflow-auto flex flex-col justify-center">
          <h2 className="text-gray-50 m-2 font-medium">Page- {pageNo}</h2>

          <div className="text-white border-separate space-y-6 text-sm overflow-auto">
            <thead className="bg-base-teal text-white text-xl">
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
                        <div className="cursor-pointer rounded-lg bg-gray-700 p-3 hover:bg-gray-900 ">
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

                  <td className="p-3">
                    <div className="flex max-w-3xl overflow-auto word-wrap no-scrollbar">
                      <div className="overflow-auto word-wrap no-scrollbar">
                        {data.description}
                      </div>
                    </div>
                  </td>

                  <td className="p-3">
                    {data.is_admin_approved ? (
                      <TiTick className="text-green-500 text-4xl" />
                    ) : (
                      <button
                        onClick={() => {
                          setOpen(true);
                          setProjId(data._id);
                        }}
                        className="flex justify-center w-1/8 mx-auto mt-4 bg-green-400 p-2 font-bold text-white rounded-xl"
                      >
                        Approve project
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </div>
        </div>

        <div className="fixed inline-flex w-full bottom-0 left-1/2 mb-32">
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
        <ProjectVisibility
          projectId={projId}
          close={() => setOpen(false)}
          isOpen={open}
        />
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

export default ProjectApplications;
