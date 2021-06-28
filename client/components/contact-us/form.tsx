const Right = () => {
  return (
    <section className="w-full max-w-2xl px-6 py-4 mx-auto bg-white rounded-md shadow-md ">
      <div className="mt-6 ">
        <div className="items-center -mx-2 md:flex">
          <div className="w-full mx-2">
            <label className="block mb-2 text-sm font-medium text-gray-600 ">
              Name
            </label>
            <input
              className="focus:border-base-teal block w-full px-4 py-2 text-gray-700  bg-white border-gray-300  border-b-2    "
              type="text"
            />
          </div>

          <div className="w-full mx-2 mt-4 md:mt-0">
            <label className="block mb-2 text-sm font-medium text-gray-600 ">
              E-mail
            </label>

            <input
              className="block focus:border-base-teal w-full px-4 py-2 text-gray-700 border-b-2 bg-white border-gray-300    "
              type="email"
            />
          </div>
        </div>

        <div className="w-full mt-4">
          <label className="block mb-2 text-sm font-medium text-gray-600 ">
            Message
          </label>

          <textarea className="block w-full h-40 px-4 py-2 border-b-2 text-gray-700 bg-white border-gray-300   focus:border-base-teal"></textarea>
        </div>

        <div className="flex justify-center mt-6">
          <button className="px-4 py-2 text-white transition-colors duration-200 transform bg-base-teal rounded-md hover:bg-gray-600   focus:bg-base-green">
            Send Message
          </button>
        </div>
      </div>
    </section>
  );
};

export default Right;
