import Next from "../../utils/icons/next";
import Previous from "../../utils/icons/previous";

const PaginationButtons = ({ hasNextPage, hasPrevPage, pageNo, setPageNo }) => {
  return (
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
        <span className="text-2xl font-extrabold">
          <Previous />
        </span>
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
        <span className="text-2xl font-extrabold">
          <Next />
        </span>
      </button>
    </div>
  );
};

export default PaginationButtons;
