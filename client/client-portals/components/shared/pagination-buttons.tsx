import { Next, Previous, First, Last } from "@/icons/index";

const PaginationButtons = ({ hasNextPage, hasPrevPage, pageNo, setPageNo, lastPage }) => {
  return (
    <div className="flex justify-center items-center">
      <button
        disabled={!hasPrevPage}
        className={`${
          !hasPrevPage
            ? "opacity-10 cursor-not-allowed"
            : "hover:bg-base-green focus:bg-base-green"
          } p-3 rounded-full`}
        onClick={() => setPageNo(1)}
      >
        <span className="text-2xl font-extrabold">
          <First />
        </span>
      </button>
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
      <button
        disabled={!hasNextPage}
        className={`${
          !hasNextPage
            ? "opacity-10 cursor-not-allowed"
            : "hover:bg-base-green focus:bg-base-green"
          } p-3 rounded-full`}
        onClick={() => setPageNo(lastPage)}
      >
        <span className="text-2xl font-extrabold">
          <Last />
        </span>
      </button>
    </div>
  );
};

export default PaginationButtons;
