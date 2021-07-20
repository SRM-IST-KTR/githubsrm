import React, { useState, useEffect } from "react";
import { getAcceptedProjects } from "services/api";
import { Card, PaginationButtons, CSSLoader, Layout } from "@/shared/index";

const AcceptedProjectsCards = () => {
  const [acceptedProjects, setAcceptedProjects] = useState([]);
  const [pageNo, setPageNo] = useState<number>(1);
  const [hasNextPage, sethasNextPage] = useState<boolean>(false);
  const [hasPrevPage, sethasPrevPage] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  const _getAcceptedProjects = async () => {
    const token = sessionStorage.getItem("token");
    const res = await getAcceptedProjects(pageNo, token);
    if (res) {
      setAcceptedProjects(res.records);
      sethasNextPage(res.hasNextPage);
      sethasPrevPage(res.hasPreviousPage);
      setLoading(false);
    }
  };

  useEffect(() => {
    _getAcceptedProjects();
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
      <PaginationButtons
        hasNextPage={hasNextPage}
        hasPrevPage={hasPrevPage}
        pageNo={pageNo}
        setPageNo={setPageNo}
      />
    </>
  ) : (
    <Layout type="admin">
      <CSSLoader />
    </Layout>
  );
};

export default AcceptedProjectsCards;
