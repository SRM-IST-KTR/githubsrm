import React, { useEffect, useState } from "react";
import instance from "services/api";
import Link from "next/link";
import { Layout, Footer, CSSLoader } from "@/shared/index";
import { TableProjectsProps } from "utils/interfaces";
import ProjectVisibility from "./project-visibility-popup";
import Tick from "utils/icons/tick";
import { PaginationButtons } from "@/shared/index";

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
        <div className="overflow-auto flex flex-col items-center justify-center">
          {tableDataProjects?.length > 0 ? (
            <h2 className="text-gray-50 m-2 font-medium">Page- {pageNo}</h2>
          ) : (
            <h2 className="text-gray-50 my-10 font-bold text-4xl">
              No Project Applications!
            </h2>
          )}

          <div className="text-white border-separate space-y-6 text-sm overflow-auto">
            <thead className="bg-base-teal text-white text-xl">
              <tr>
                {tableDataProjects.length > 0 &&
                  headings.map((head) => (
                    <th key={head} className="px-3 text-left">
                      {head}
                    </th>
                  ))}
              </tr>
            </thead>

            <tbody>
              {tableDataProjects?.map((data) => (
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
                      <span className="text-green-500 text-4xl">
                        <Tick />
                      </span>
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
        {tableDataProjects.length > 0 && (
          <PaginationButtons
            hasNextPage={hasNextPage}
            hasPrevPage={hasPrevPage}
            pageNo={pageNo}
            setPageNo={setPageNo}
          />
        )}
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
    <>
      <Layout type="admin">
        <div className="flex flex-col items-center justify-center">
          <CSSLoader />
        </div>
      </Layout>
      <div className="fixed bottom-0 w-full">
        <Footer />
      </div>
    </>
  );
};

export default ProjectApplications;
