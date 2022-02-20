interface PdfDiaplayProps {
  source: {
    href: string;
    title?: string;
    subTitle?: string;
    content?: string;
    name?: string;
    icon?: JSX.Element;
  };
}

const PdfDisplay = ({ source }: PdfDiaplayProps) => {
  return (
    <>
      <div key={source.name} className="">
        <div className=" h-screen my-5 shadow-xl ">
          <iframe
            src={source.href}
            height="100%"
            width="100%"
            className="rounded-lg"
          ></iframe>
        </div>
      </div>
    </>
  );
};

export default PdfDisplay;
