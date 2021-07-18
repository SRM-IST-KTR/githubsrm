import Card from "../../../shared/card";
import React, { useState, useEffect } from "react";
import { GrNext, GrPrevious } from "react-icons/gr";
import { AcceptedProjectProps } from "../../../../utils/interfaces";
import { getAcceptedProjects } from "../../../../services/api";
import CSSLoader from "../../../shared/loader";

const AcceptedProjectsCards = () => {
  const [acceptedProjects, setAcceptedProjects] = useState<
    AcceptedProjectProps[]
  >([]);
  const [pageNo, setPageNo] = useState<number>(1);
  const [hasNextPage, sethasNextPage] = useState<boolean>(false);
  const [hasPrevPage, sethasPrevPage] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    let mounted = true;
    const token = sessionStorage.getItem("token");
    const res = getAcceptedProjects(pageNo, token);
    if (res) {
      if (mounted) {
        //@ts-ignore
        setAcceptedProjects(res.records);
        //@ts-ignore
        sethasNextPage(res.hasNextPage);
        //@ts-ignore
        sethasPrevPage(res.hasPreviousPage);
        setLoading(false);
      }
    }
    console.log(acceptedProjects);
    return () => {
      mounted = false;
    };
  }, [pageNo]);

  return !loading ? (
    <>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 ">
        {acceptedProjects?.map((item) => (
          <Card
            url={`/admin/dashboard/accepted-projects/${item._id}`}
            name={item.project_name}
            desc={item.description}
            key={item._id}
          />
        ))}
      </div>

      <div className="flex justify-center my-14">
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
    </>
  ) : (
    <div className="flex flex-col items-center justify-center w-screen min-h-screen bg-base-blue">
      <CSSLoader />
    </div>
  );
};

export default AcceptedProjectsCards;
