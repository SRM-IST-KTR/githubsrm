const SectionIcon = ({ name, sec, click, _key }) => {
  return (
    <div key={_key} onClick={() => click()} className="relative flex fex-col">
      <div className={(!sec ? "text-base-green" : "") + " w-3/4"}>{name}</div>
      <div className="w-full">
        <div className=" relative w-full h-full">
          <div className="mx-auto w-1 bg-black h-full"></div>
          <div
            className={
              (sec ? "invisible" : " ") +
              " absolute left-1/2 bottom-1/2 rounded-full   bg-base-green w-5 h-5"
            }
          ></div>
        </div>
      </div>
    </div>
  );
};

export default SectionIcon;
