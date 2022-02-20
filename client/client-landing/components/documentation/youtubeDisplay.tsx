interface LinkProps {
  source: {
    href: string;
    title?: string;
    subTitle?: string;
    content?: string;
    name?: string;
    icon?: JSX.Element;
  };
}

const YoutubeDisplay = ({ source }: LinkProps) => {
  return (
    <>
      <div className="flex flex-col justify-center items-center">
        <div className="flex flex-col justify-center items-center my-7">
          <div className="text-4xl font-medium">{source.title}</div>
          <div className="text-xl mt-2 font-medium">{source.subTitle}</div>
        </div>
        <div className="flex flex-col bg-white rounded-lg justify-center items-center ">
          <div className="pt-10 px-5 lg:px-20">{source.content}</div>
          <div className="m-5 w-12/12 lg:w-7/12 h-3/6">
            <iframe
              className="rounded-lg"
              width="100%"
              height="230px"
              src={source.href}
              title={source.title}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            ></iframe>
          </div>
        </div>
      </div>
    </>
  );
};

export default YoutubeDisplay;
