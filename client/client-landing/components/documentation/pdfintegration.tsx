import { useState } from "react";
import { ArrowIcon } from '../../utils/icons'
const PdfFile = () => {
    const sources: {
        name: string,
        href: string,
        icon: JSX.Element
    }[] = [{
        name: "Sample PDF",
        href: "https://drive.google.com/file/d/1kPcD_GpBODXD6pUgfLaqPhEHwpB-lpk3/preview",
        icon: <ArrowIcon />
    },
    {
        name: "Lab PDF",
        href: "https://drive.google.com/file/d/1LZzQP5RPTMI4RKzTpnwfA3ufnc60Z2zA/preview",
        icon: <ArrowIcon />
    },
    {
        name: "Paralinguistic PDF",
        href: "https://drive.google.com/file/d/1-Ktm3gE9WWDxnT_wvUON1VudSRb6dM8i/preview",
        icon: <ArrowIcon />
    }
    ]
    let [pdfHref, setPdfHref] = useState<string>(sources[0].href);


    return (
        <div>
            <br/>
            <p className="text-3xl my-3">PDF Tutorial</p>

            <div className="flex flex-col md:flex-row justify-evenly mt-8">
                <div className="w-full md:w-4/12 flex flex-col sm:flex-row md:flex-col">
                    {sources.map((source) => (
                        <div key={source.name} className="flex mx-2 w-full">
                            <div
                                onClick={() => setPdfHref(source.href)}
                                className={`${pdfHref === source.href
                                    ? "border-base-green"
                                    : "md:border-transparent"
                                    } border-b-4 md:border-b-0 md:border-r-4 w-full cursor-pointer py-4 flex items-center justify-between transform hover:md:-translate-x-4`}
                            >
                                <div>
                                    <h3 className={`${pdfHref === source.href ? "font-medium" : ""} text-xl mb-2`}>
                                        {source.name}
                                    </h3>
                                </div>

                                <div className="mx-4">
                                    <span
                                        className={`${pdfHref === source.href
                                            ? "bg-base-green bg-opacity-80"
                                            : "bg-base-smoke"
                                            } w-12 hidden md:flex justify-center items-center p-2 rounded-full`}
                                    >
                                        {source.icon}
                                    </span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="w-full md:px-8 mt-8 md:mt-0">
                    <div className="px-8 py-4 lg:px-8 bg-gray-100 border-t-8 rounded-sm border-base-green">
                        {sources.map(
                            (source) =>
                                source.href === pdfHref && (
                                    <div key={source.name} className="">
                                        <div className=" h-screen my-5 shadow-xl ">
                                            <iframe src={source.href} height="100%" width="100%" className="rounded-lg"></iframe>
                                        </div>
                                    </div>
                                ))}
                    </div>
                </div>
            </div>
        </div>)
}

export default PdfFile;