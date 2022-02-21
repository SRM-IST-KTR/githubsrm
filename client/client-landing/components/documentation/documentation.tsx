import { useState } from "react";
import { ArrowIcon } from "../../utils/icons";
import PdfDisplay from "./pdfDisplay";
import PdfSideBarLink from "./pdfSideBarLink";
import YoutubeDisplay from "./youtubeDisplay";
import YoutubeSideBarLink from "./YoutubeSideBarLinks";

/*
  pdfSources (array of Objects) to store name and url of the PDF.
*/
const Documentation = () => {
  const pdfSources: {
    name: string;
    href: string;
  }[] = [
      {
        name: "Sample PDF",
        href: "https://drive.google.com/file/d/1kPcD_GpBODXD6pUgfLaqPhEHwpB-lpk3/preview",
      },
      {
        name: "Lab PDF",
        href: "https://drive.google.com/file/d/1LZzQP5RPTMI4RKzTpnwfA3ufnc60Z2zA/preview",
      },
      {
        name: "Paralinguistic PDF",
        href: "https://drive.google.com/file/d/1-Ktm3gE9WWDxnT_wvUON1VudSRb6dM8i/preview",
      },
    ];

  /*
  youtubeSources (array of Objects) to store name and url of the Youtube Videos/Local Videos address..
  */
  const youtubeSources: {
    title: string;
    subTitle: string;
    content: string;
    href: string;
  }[] = [
      {
        title: "C++ in 100 Seconds",
        subTitle: "Fireship",
        content:
          "C++ or C-plus-plus or Cpp is an extremely popular object-oriented programming language. Created in 1979, today it powers game engines, databases, compilers, embedded systems, desktop software, and much of our software infrastructure. ",
        href: "https://www.youtube.com/embed/MNeX4EGtR5Y",
      },
      {
        title: "Firebase in 100 Seconds",
        subTitle: "Fireship",
        content:
          "Firebase is a suite of tools for building apps on top of Google Cloud Platform. It's most famous for its realtime database, but also includes services for user authentication, serverless computing, push messaging, file storage, and more.",
        href: "https://www.youtube.com/embed/vAoB4VbhRzM",
      },
      {
        title: "GraphQL Explained in 100 Seconds",
        subTitle: "Fireship",
        content:
          "What is GraphQL? Learn how it compares to REST and why developers love this query language for reading and mutating data in APIs",
        href: "https://www.youtube.com/embed/eIQh02xuVw4",
      },
    ];

  const [display, setDisplay] = useState({
    source: pdfSources[1],
    type: "PDF",
  });

  return (
    <div>
      <h1 className="text-5xl lg:text-5xl font-extrabold text-base-blue">
        Documentation
      </h1>
      <hr />
      <div>
        <br />

        <div className="flex flex-col md:flex-row justify-evenly mt-8">
          <div className="w-full md:w-4/12 flex flex-col md:flex-row md:flex-col">
            {/* Pdf Navigation Bar */}
            <PdfSideBarLink
              fnc={setDisplay}
              icon={<ArrowIcon />}
              sources={pdfSources}
              current={display.source.href}
              /> 
            {/* Video Navigation Bar */}
            <YoutubeSideBarLink
              icon={<ArrowIcon />}
              fnc={setDisplay}
              sources={youtubeSources}
              current={display.source.href}
            />
          </div>
          <div className="w-full md:px-8 mt-8 md:mt-0">
            <div className="px-4 md:px-8 py-4 lg:px-8 bg-gray-100 border-t-8 rounded-sm border-base-green">
              {/* Content elements which displayes according to the selection in Side Bar */}
              {display.type === "PDF" ? (
                <PdfDisplay source={display.source} />
              ) : (
                <YoutubeDisplay source={display.source} />
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Documentation;
